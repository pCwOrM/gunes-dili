"""
Güneş Dili Programlama Dili (Güneş-Lang) — Soyut Sözdizim Ağacı (AST Düğümleri)
=============================================================================
Dilin mantıksal sözdizimini temsil eden tip güvenli AST sınıfları.
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from .tokens import Token


class ASTNode:
    pass


# ---------------------------------------------------------------------------
# İfadeler (Expressions - Değer Üreten Yapılar)
# ---------------------------------------------------------------------------

@dataclass
class Expr(ASTNode):
    pass


@dataclass
class LiteralExpr(Expr):
    value: Any


@dataclass
class VariableExpr(Expr):
    name: Token


@dataclass
class BinaryExpr(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass
class UnaryExpr(Expr):
    operator: Token
    right: Expr


@dataclass
class CallExpr(Expr):
    callee: Expr
    paren: Token
    arguments: List[Expr]


@dataclass
class ListExpr(Expr):
    elements: List[Expr]


@dataclass
class IndexExpr(Expr):
    target: Expr
    bracket: Token
    index: Expr


@dataclass
class AssignExpr(Expr):
    name: Token
    value: Expr


# ---------------------------------------------------------------------------
# Deyimler (Statements - Durum Değiştiren veya Akış Kontrol Eden Yapılar)
# ---------------------------------------------------------------------------

@dataclass
class Stmt(ASTNode):
    pass


@dataclass
class ExprStmt(Stmt):
    expression: Expr


@dataclass
class VarDeclStmt(Stmt):
    name: Token
    initializer: Optional[Expr]


@dataclass
class BlockStmt(Stmt):
    statements: List[Stmt]


@dataclass
class IfStmt(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Optional[Stmt]


@dataclass
class WhileStmt(Stmt):
    condition: Expr
    body: Stmt


@dataclass
class FunctionStmt(Stmt):
    name: Token
    params: List[Token]
    body: List[Stmt]


@dataclass
class ReturnStmt(Stmt):
    keyword: Token
    value: Optional[Expr]


@dataclass
class PrintStmt(Stmt):
    keyword: Token
    expression: Expr


@dataclass
class BreakStmt(Stmt):
    keyword: Token


@dataclass
class ContinueStmt(Stmt):
    keyword: Token


@dataclass
class Program(ASTNode):
    statements: List[Stmt]
