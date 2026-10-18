"""
Güneş Dili Programlama Dili (Güneş-Lang) — Deterministik Sözcük Çözümleyici (Lexer)
==================================================================================
Lean 4 ispatlarıyla doğrulanmış kurallara göre tek geçişli, geri izlemesiz (O(L))
deterministik ayrıştırma gerçekleştirir.
"""

from typing import List, Optional, Any
from .tokens import Token, TokenType, KEYWORDS


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Sözdizim Hatası (Satır {line}, Sütun {column}): {message}")
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.token_start_column = 1

    def tokenize(self) -> List[Token]:
        while not self._is_at_end():
            self.start = self.current
            self.token_start_column = self.column
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column))
        return self.tokens

    def _scan_token(self) -> None:
        c = self._advance()

        # Boşluklar ve satır sonları
        if c in ' \r\t':
            return
        elif c == '\n':
            self.line += 1
            self.column = 1
            return

        # Yorum satırları (-- Lean 4 / Haskell tarzı)
        if c == '-' and self._match('-'):
            while self._peek() != '\n' and not self._is_at_end():
                self._advance()
            return

        # Yorum bloğu (/* ... */)
        if c == '/' and self._match('*'):
            while not (self._peek() == '*' and self._peek_next() == '/') and not self._is_at_end():
                if self._peek() == '\n':
                    self.line += 1
                    self.column = 0
                self._advance()
            if not self._is_at_end():
                self._advance()  # *
                self._advance()  # /
            else:
                raise LexerError("Kapatılmamış yorum bloğu", self.line, self.column)
            return

        # Tek karakterlik ayraçlar
        if c == '(':
            self._add_token(TokenType.LPAREN)
        elif c == ')':
            self._add_token(TokenType.RPAREN)
        elif c == '{':
            self._add_token(TokenType.LBRACE)
        elif c == '}':
            self._add_token(TokenType.RBRACE)
        elif c == '[':
            self._add_token(TokenType.LBRACKET)
        elif c == ']':
            self._add_token(TokenType.RBRACKET)
        elif c == ';':
            self._add_token(TokenType.SEMICOLON)
        elif c == ',':
            self._add_token(TokenType.COMMA)

        # Sembolik işleçler
        elif c == '+':
            self._add_token(TokenType.KAT)
        elif c == '-':
            if self._match('>'):
                self._add_token(TokenType.ARROW)
            else:
                self._add_token(TokenType.KES)
        elif c == '*':
            self._add_token(TokenType.TARAP)
        elif c == '/':
            self._add_token(TokenType.BOL)
        elif c == '%':
            self._add_token(TokenType.KALAN)
        elif c == '=':
            if self._match('='):
                self._add_token(TokenType.ES)
            else:
                self._add_token(TokenType.YI)  # = sembolü de 'yi' yerine geçebilir
        elif c == '!':
            if self._match('='):
                self._add_token(TokenType.ESDE)
            else:
                self._add_token(TokenType.DEGIL)
        elif c == '<':
            if self._match('='):
                self._add_token(TokenType.KUTUKES)
            else:
                self._add_token(TokenType.KUTUK)
        elif c == '>':
            if self._match('='):
                self._add_token(TokenType.BUYUKES)
            else:
                self._add_token(TokenType.BUYUK)
        elif c == '&' and self._match('&'):
            self._add_token(TokenType.VE)
        elif c == '|' and self._match('|'):
            self._add_token(TokenType.VEYA)

        # Dizgiler (Strings) - Çift ve Tek Tırnak Desteği
        elif c in ('"', "'"):
            self._string(quote_char=c)

        # Sayılar (Numbers)
        elif c.isdigit():
            self._number()

        # Tanımlayıcılar ve Güneş Dili anahtar sözcükleri
        elif c.isalpha() or c == '_':
            self._identifier()

        else:
            raise LexerError(f"Bilinmeyen karakter: '{c}'", self.line, self.token_start_column)

    def _string(self, quote_char: str = '"') -> None:
        chars = []
        while self._peek() != quote_char and not self._is_at_end():
            if self._peek() == '\n':
                self.line += 1
                self.column = 0
            if self._peek() == '\\':
                self._advance()
                esc = self._advance()
                if esc == 'n':
                    chars.append('\n')
                elif esc == 't':
                    chars.append('\t')
                elif esc == '"':
                    chars.append('"')
                elif esc == "'":
                    chars.append("'")
                elif esc == '\\':
                    chars.append('\\')
                else:
                    chars.append(esc)
            else:
                chars.append(self._advance())

        if self._is_at_end():
            raise LexerError("Kapatılmamış metin dizgisi", self.line, self.token_start_column)

        self._advance()  # Kapanış tırnağı
        value = "".join(chars)
        self._add_token(TokenType.STRING, value)

    def _number(self) -> None:
        while self._peek().isdigit():
            self._advance()

        # Kayan noktalı sayı kontrolü
        if self._peek() == '.' and self._peek_next().isdigit():
            self._advance()  # '.' karakterini tüket
            while self._peek().isdigit():
                self._advance()
            val = float(self.source[self.start:self.current])
        else:
            val = int(self.source[self.start:self.current])

        self._add_token(TokenType.NUMBER, val)

    def _identifier(self) -> None:
        while self._peek().isalnum() or self._peek() == '_':
            self._advance()

        text = self.source[self.start:self.current].lower()
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)

        if token_type == TokenType.BOOLEAN:
            literal = (text == "dogru")
        else:
            literal = None

        self._add_token(token_type, literal)

    def _advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        self.column += 1
        return c

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return '\0'
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _add_token(self, token_type: TokenType, literal: Any = None) -> None:
        lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, lexeme, literal, self.line, self.token_start_column))
