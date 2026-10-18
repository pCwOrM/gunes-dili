"""
Güneş Dili Programlama Dili (Güneş-Lang) — Çalışma Zamanı Bellek ve Kapsam Modeli (Environment)
=============================================================================================
Sıfır bellek sızıntılı, leksikal kapsam (lexical scoping) destekleyen sembol tablosu.
"""

from typing import Dict, Any, Optional
from .tokens import Token


class RuntimeError(Exception):
    def __init__(self, token: Optional[Token], message: str):
        if token:
            super().__init__(f"Çalışma Zamanı Hatası (Satır {token.line}, Sütun {token.column}): {message} ('{token.lexeme}')")
        else:
            super().__init__(f"Çalışma Zamanı Hatası: {message}")
        self.token = token


class Environment:
    def __init__(self, enclosing: Optional['Environment'] = None):
        self.values: Dict[str, Any] = {}
        self.enclosing: Optional['Environment'] = enclosing

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def get(self, name_token: Token) -> Any:
        lexeme = name_token.lexeme.lower()
        if lexeme in self.values:
            return self.values[lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(name_token)

        raise RuntimeError(name_token, f"Tanımsız değişken: '{name_token.lexeme}'")

    def assign(self, name_token: Token, value: Any) -> None:
        lexeme = name_token.lexeme.lower()
        if lexeme in self.values:
            self.values[lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name_token, value)
            return

        raise RuntimeError(name_token, f"Atama yapılamadı, tanımsız değişken: '{name_token.lexeme}'")
