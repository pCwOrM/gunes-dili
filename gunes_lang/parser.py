"""
Güneş Dili Programlama Dili (Güneş-Lang) — Sözdizimsel Çözümleyici (Parser)
===========================================================================
Güneş Dili gramer kurallarını recursive descent (özyinelemeli iniş) yöntemiyle
deterministik olarak AST ağacına dönüştürür.
"""

from typing import List, Optional
from .tokens import Token, TokenType
from .ast_nodes import (
    Expr, Stmt, LiteralExpr, VariableExpr, BinaryExpr, UnaryExpr,
    CallExpr, ListExpr, IndexExpr, AssignExpr, ExprStmt, VarDeclStmt,
    BlockStmt, IfStmt, WhileStmt, FunctionStmt, ReturnStmt, PrintStmt,
    BreakStmt, ContinueStmt, Program
)


class ParserError(Exception):
    def __init__(self, message: str, token: Token):
        super().__init__(f"Ayrıştırma Hatası (Satır {token.line}, Sütun {token.column}): {message} ('{token.lexeme}' yakınında)")
        self.token = token


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        statements: List[Stmt] = []
        
        # Eğer program 'ag { ... }' bloğu ile başlıyorsa
        if self._match(TokenType.AG):
            self._consume(TokenType.LBRACE, "Güneş bloğu 'ag' sonrası '{' bekleniyor.")
            ag_block = self._block_statements()
            return Program(statements=ag_block)

        while not self._is_at_end():
            stmt = self._declaration()
            if stmt is not None:
                statements.append(stmt)
        return Program(statements=statements)

    # -----------------------------------------------------------------------
    # Bildirimler (Declarations)
    # -----------------------------------------------------------------------

    def _declaration(self) -> Optional[Stmt]:
        try:
            if self._match(TokenType.TAN):
                return self._var_declaration()
            if self._match(TokenType.TANIM):
                return self._function_declaration()
            return self._statement()
        except ParserError as error:
            self._synchronize()
            raise error

    def _var_declaration(self) -> VarDeclStmt:
        name = self._consume(TokenType.IDENTIFIER, "Değişken adı bekleniyor.")
        initializer = None
        if self._match(TokenType.YI):
            initializer = self._expression()
        self._consume(TokenType.SEMICOLON, "Değişken bildiriminden sonra ';' bekleniyor.")
        return VarDeclStmt(name=name, initializer=initializer)

    def _function_declaration(self) -> FunctionStmt:
        name = self._consume(TokenType.IDENTIFIER, "İşlev (fonksiyon) adı bekleniyor.")
        self._consume(TokenType.LPAREN, "İşlev adından sonra '(' bekleniyor.")
        params: List[Token] = []
        if not self._check(TokenType.RPAREN):
            while True:
                params.append(self._consume(TokenType.IDENTIFIER, "Parametre adı bekleniyor."))
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RPAREN, "Parametre listesinden sonra ')' bekleniyor.")
        self._consume(TokenType.LBRACE, "İşlev gövdesinden önce '{' bekleniyor.")
        body = self._block_statements()
        return FunctionStmt(name=name, params=params, body=body)

    # -----------------------------------------------------------------------
    # Deyimler (Statements)
    # -----------------------------------------------------------------------

    def _statement(self) -> Stmt:
        if self._match(TokenType.WERLA):
            return self._print_statement()
        if self._match(TokenType.WER):
            return self._return_statement()
        if self._match(TokenType.BAKBA):
            return self._if_statement()
        if self._match(TokenType.DONKE):
            return self._while_statement()
        if self._match(TokenType.DUR):
            keyword = self._previous()
            self._consume(TokenType.SEMICOLON, "'dur' deyiminden sonra ';' bekleniyor.")
            return BreakStmt(keyword=keyword)
        if self._match(TokenType.GEC):
            keyword = self._previous()
            self._consume(TokenType.SEMICOLON, "'gec' deyiminden sonra ';' bekleniyor.")
            return ContinueStmt(keyword=keyword)
        if self._match(TokenType.LBRACE):
            return BlockStmt(statements=self._block_statements())
        return self._expression_statement()

    def _print_statement(self) -> PrintStmt:
        keyword = self._previous()
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "'werla' değerinden sonra ';' bekleniyor.")
        return PrintStmt(keyword=keyword, expression=value)

    def _return_statement(self) -> ReturnStmt:
        keyword = self._previous()
        value = None
        if not self._check(TokenType.SEMICOLON):
            value = self._expression()
        self._consume(TokenType.SEMICOLON, "'wer' deyiminden sonra ';' bekleniyor.")
        return ReturnStmt(keyword=keyword, value=value)

    def _if_statement(self) -> IfStmt:
        self._consume(TokenType.LPAREN, "'bakba' sonrasında '(' bekleniyor.")
        condition = self._expression()
        self._consume(TokenType.RPAREN, "Koşul ifadesinden sonra ')' bekleniyor.")
        then_branch = self._statement()
        else_branch = None
        if self._match(TokenType.BAKDE):
            else_branch = self._statement()
        return IfStmt(condition=condition, then_branch=then_branch, else_branch=else_branch)

    def _while_statement(self) -> WhileStmt:
        self._consume(TokenType.LPAREN, "'donke' sonrasında '(' bekleniyor.")
        condition = self._expression()
        self._consume(TokenType.RPAREN, "Döngü koşulundan sonra ')' bekleniyor.")
        body = self._statement()
        return WhileStmt(condition=condition, body=body)

    def _block_statements(self) -> List[Stmt]:
        statements: List[Stmt] = []
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            stmt = self._declaration()
            if stmt is not None:
                statements.append(stmt)
        self._consume(TokenType.RBRACE, "Blok sonunda '}' bekleniyor.")
        return statements

    def _expression_statement(self) -> ExprStmt:
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "İfadeden sonra ';' bekleniyor.")
        return ExprStmt(expression=expr)

    # -----------------------------------------------------------------------
    # İfadeler ve İşleç Öncelikleri (Expressions)
    # -----------------------------------------------------------------------

    def _expression(self) -> Expr:
        return self._assignment()

    def _assignment(self) -> Expr:
        expr = self._logic_or()

        if self._match(TokenType.YI):
            equals = self._previous()
            value = self._assignment()

            if isinstance(expr, VariableExpr):
                return AssignExpr(name=expr.name, value=value)
            raise ParserError("Geçersiz atama hedefi.", equals)

        return expr

    def _logic_or(self) -> Expr:
        expr = self._logic_and()
        while self._match(TokenType.VEYA):
            op = self._previous()
            right = self._logic_and()
            expr = BinaryExpr(left=expr, operator=op, right=right)
        return expr

    def _logic_and(self) -> Expr:
        expr = self._equality()
        while self._match(TokenType.VE):
            op = self._previous()
            right = self._equality()
            expr = BinaryExpr(left=expr, operator=op, right=right)
        return expr

    def _equality(self) -> Expr:
        expr = self._comparison()
        while self._match(TokenType.ES, TokenType.ESDE):
            op = self._previous()
            right = self._comparison()
            expr = BinaryExpr(left=expr, operator=op, right=right)
        return expr

    def _comparison(self) -> Expr:
        expr = self._term()
        while self._match(TokenType.BUYUK, TokenType.BUYUKES, TokenType.KUTUK, TokenType.KUTUKES):
            op = self._previous()
            right = self._term()
            expr = BinaryExpr(left=expr, operator=op, right=right)
        return expr

    def _term(self) -> Expr:
        expr = self._factor()
        while self._match(TokenType.KAT, TokenType.KES):
            op = self._previous()
            right = self._factor()
            expr = BinaryExpr(left=expr, operator=op, right=right)
        return expr

    def _factor(self) -> Expr:
        expr = self._unary()
        while self._match(TokenType.TARAP, TokenType.BOL, TokenType.KALAN):
            op = self._previous()
            right = self._unary()
            expr = BinaryExpr(left=expr, operator=op, right=right)
        return expr

    def _unary(self) -> Expr:
        if self._match(TokenType.DEGIL, TokenType.KES):
            op = self._previous()
            right = self._unary()
            return UnaryExpr(operator=op, right=right)
        return self._call()

    def _call(self) -> Expr:
        expr = self._primary()

        while True:
            if self._match(TokenType.LPAREN):
                expr = self._finish_call(expr)
            elif self._match(TokenType.LBRACKET):
                bracket = self._previous()
                index = self._expression()
                self._consume(TokenType.RBRACKET, "Dizi erişiminde ']' bekleniyor.")
                expr = IndexExpr(target=expr, bracket=bracket, index=index)
            else:
                break

        return expr

    def _finish_call(self, callee: Expr) -> CallExpr:
        paren = self._previous()
        arguments: List[Expr] = []
        if not self._check(TokenType.RPAREN):
            while True:
                arguments.append(self._expression())
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RPAREN, "Argüman listesinden sonra ')' bekleniyor.")
        return CallExpr(callee=callee, paren=paren, arguments=arguments)

    def _primary(self) -> Expr:
        if self._match(TokenType.BOOLEAN):
            return LiteralExpr(value=self._previous().literal)
        if self._match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(value=self._previous().literal)
        if self._match(TokenType.IDENTIFIER):
            return VariableExpr(name=self._previous())

        if self._match(TokenType.LPAREN):
            expr = self._expression()
            self._consume(TokenType.RPAREN, "İfade sonrası ')' bekleniyor.")
            return expr

        # Dizi / Liste değişmezi: [1, 2, 3]
        if self._match(TokenType.LBRACKET):
            elements: List[Expr] = []
            if not self._check(TokenType.RBRACKET):
                while True:
                    elements.append(self._expression())
                    if not self._match(TokenType.COMMA):
                        break
            self._consume(TokenType.RBRACKET, "Dizi sonrasında ']' bekleniyor.")
            return ListExpr(elements=elements)

        raise ParserError(f"Beklenmeyen ifade: '{self._peek().lexeme}'", self._peek())

    # -----------------------------------------------------------------------
    # Yardımcı Yöntemler
    # -----------------------------------------------------------------------

    def _match(self, *types: TokenType) -> bool:
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise ParserError(message, self._peek())

    def _synchronize(self) -> None:
        self._advance()
        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return
            if self._peek().type in (TokenType.TAN, TokenType.TANIM, TokenType.BAKBA,
                                     TokenType.DONKE, TokenType.WER, TokenType.WERLA):
                return
            self._advance()
