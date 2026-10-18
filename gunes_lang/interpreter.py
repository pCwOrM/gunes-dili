"""
Güneş Dili Programlama Dili (Güneş-Lang) — Yorumlayıcı ve Çalışma Zamanı Motoru (Interpreter)
===========================================================================================
Güneş Dili AST ağacını doğrudan yorumlar, WERR telemetrisini işletir ve çıktıyı üretir.
"""

import time
import sys
from typing import Any, List, Optional, Callable
from .tokens import Token, TokenType
from .ast_nodes import (
    Expr, Stmt, LiteralExpr, VariableExpr, BinaryExpr, UnaryExpr,
    CallExpr, ListExpr, IndexExpr, AssignExpr, ExprStmt, VarDeclStmt,
    BlockStmt, IfStmt, WhileStmt, FunctionStmt, ReturnStmt, PrintStmt,
    BreakStmt, ContinueStmt, Program
)
from .environment import Environment, RuntimeError
from .telemetry import WerrTelemetry


class ReturnException(Exception):
    def __init__(self, value: Any):
        self.value = value


class BreakException(Exception):
    pass


class ContinueException(Exception):
    pass


class CallableFunction:
    def __init__(self, declaration: FunctionStmt, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter: 'Interpreter', arguments: List[Any]) -> Any:
        environment = Environment(enclosing=self.closure)
        for i, param in enumerate(self.declaration.params):
            val = arguments[i] if i < len(arguments) else None
            environment.define(param.lexeme.lower(), val)

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as ret:
            return ret.value
        return None

    def arity(self) -> int:
        return len(self.declaration.params)

    def __repr__(self) -> str:
        return f"<işlev {self.declaration.name.lexeme}>"


class BuiltinFunction:
    def __init__(self, name: str, arity: int, func: Callable[..., Any]):
        self.name = name
        self._arity = arity
        self.func = func

    def call(self, interpreter: 'Interpreter', arguments: List[Any]) -> Any:
        return self.func(*arguments)

    def arity(self) -> int:
        return self._arity

    def __repr__(self) -> str:
        return f"<yerleşik-işlev {self.name}>"


class Interpreter:
    def __init__(self, output_callback: Optional[Callable[[str], None]] = None):
        self.globals = Environment()
        self.environment = self.globals
        self.telemetry = WerrTelemetry()
        self.output_callback = output_callback or (lambda text: print(text))
        self.output_buffer: List[str] = []

        self._define_builtins()

    def _define_builtins(self) -> None:
        # boy / uzunluk
        self.globals.define("boy", BuiltinFunction("boy", 1, lambda x: len(x) if hasattr(x, '__len__') else 0))
        self.globals.define("uzunluk", BuiltinFunction("uzunluk", 1, lambda x: len(x) if hasattr(x, '__len__') else 0))
        
        # ekle (dizi, eleman)
        def _ekle(arr: list, item: Any) -> list:
            if isinstance(arr, list):
                arr.append(item)
                return arr
            return arr
        self.globals.define("ekle", BuiltinFunction("ekle", 2, _ekle))

        # zaman (timestamp ms)
        self.globals.define("zaman", BuiltinFunction("zaman", 0, lambda: int(time.time() * 1000)))

        # sayi / metin dönüşümleri
        self.globals.define("sayi", BuiltinFunction("sayi", 1, lambda x: int(x) if str(x).isdigit() else float(x)))
        self.globals.define("metin", BuiltinFunction("metin", 1, lambda x: str(x)))

        # WERR 53-Hölder rezonans tonu sorgusu
        self.globals.define("rezonans", BuiltinFunction("rezonans", 1, lambda s: sum(ord(c) for c in str(s)) % 53))

    def interpret(self, program: Program) -> Any:
        result = None
        try:
            for stmt in program.statements:
                result = self.execute(stmt)
            return result
        except RuntimeError as err:
            self._print_output(f"HATA: {err}")
            raise err

    def execute(self, stmt: Stmt) -> Any:
        self.telemetry.record(stmt.__class__.__name__)

        if isinstance(stmt, ExprStmt):
            return self.evaluate(stmt.expression)
        elif isinstance(stmt, PrintStmt):
            val = self.evaluate(stmt.expression)
            formatted = self._format_value(val)
            self._print_output(formatted)
            return val
        elif isinstance(stmt, VarDeclStmt):
            val = None
            if stmt.initializer is not None:
                val = self.evaluate(stmt.initializer)
            lexeme = stmt.name.lexeme.lower()
            if self.environment.enclosing is not None and self._find_in_ancestor(self.environment.enclosing, lexeme):
                self.environment.assign(stmt.name, val)
            else:
                self.environment.define(lexeme, val)
            return val
        elif isinstance(stmt, BlockStmt):
            return self.execute_block(stmt.statements, Environment(enclosing=self.environment))
        elif isinstance(stmt, IfStmt):
            condition = self.evaluate(stmt.condition)
            if self._is_truthy(condition):
                return self.execute(stmt.then_branch)
            elif stmt.else_branch is not None:
                return self.execute(stmt.else_branch)
            return None
        elif isinstance(stmt, WhileStmt):
            while self._is_truthy(self.evaluate(stmt.condition)):
                try:
                    self.execute(stmt.body)
                except BreakException:
                    break
                except ContinueException:
                    continue
            return None
        elif isinstance(stmt, BreakStmt):
            raise BreakException()
        elif isinstance(stmt, ContinueStmt):
            raise ContinueException()
        elif isinstance(stmt, FunctionStmt):
            func = CallableFunction(declaration=stmt, closure=self.environment)
            self.environment.define(stmt.name.lexeme.lower(), func)
            return func
        elif isinstance(stmt, ReturnStmt):
            val = None
            if stmt.value is not None:
                val = self.evaluate(stmt.value)
            raise ReturnException(val)
        else:
            raise RuntimeError(None, f"Bilinmeyen deyim türü: {stmt.__class__.__name__}")

    def execute_block(self, statements: List[Stmt], environment: Environment) -> Any:
        previous = self.environment
        result = None
        try:
            self.environment = environment
            for statement in statements:
                result = self.execute(statement)
        finally:
            self.environment = previous
        return result

    def evaluate(self, expr: Expr) -> Any:
        if isinstance(expr, LiteralExpr):
            return expr.value
        elif isinstance(expr, VariableExpr):
            return self.environment.get(expr.name)
        elif isinstance(expr, AssignExpr):
            val = self.evaluate(expr.value)
            self.environment.assign(expr.name, val)
            return val
        elif isinstance(expr, ListExpr):
            return [self.evaluate(el) for el in expr.elements]
        elif isinstance(expr, IndexExpr):
            target = self.evaluate(expr.target)
            idx = self.evaluate(expr.index)
            if not isinstance(target, (list, str)):
                raise RuntimeError(expr.bracket, f"Dizi olmayan hedef üzerinde indeksleme yapılamaz: {type(target).__name__}")
            if not isinstance(idx, int):
                raise RuntimeError(expr.bracket, f"İndeks bir tamsayı olmalıdır, verilen: {type(idx).__name__}")
            if idx < 0 or idx >= len(target):
                raise RuntimeError(expr.bracket, f"İndeks sınır dışı: {idx} (Uzunluk: {len(target)})")
            return target[idx]
        elif isinstance(expr, UnaryExpr):
            right = self.evaluate(expr.right)
            if expr.operator.type == TokenType.DEGIL:
                return not self._is_truthy(right)
            elif expr.operator.type == TokenType.KES:
                return -right
            raise RuntimeError(expr.operator, f"Bilinmeyen tekil işleç: {expr.operator.lexeme}")
        elif isinstance(expr, BinaryExpr):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)
            op = expr.operator.type

            # Aritmetik
            if op == TokenType.KAT:
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                if isinstance(left, list) and isinstance(right, list):
                    return left + right
                return left + right
            elif op == TokenType.KES:
                return left - right
            elif op == TokenType.TARAP:
                return left * right
            elif op == TokenType.BOL:
                if right == 0:
                    raise RuntimeError(expr.operator, "Sıfıra bölme hatası.")
                return left / right
            elif op == TokenType.KALAN:
                return left % right

            # Karşılaştırma
            elif op == TokenType.ES:
                return left == right
            elif op == TokenType.ESDE:
                return left != right
            elif op == TokenType.BUYUK:
                return left > right
            elif op == TokenType.BUYUKES:
                return left >= right
            elif op == TokenType.KUTUK:
                return left < right
            elif op == TokenType.KUTUKES:
                return left <= right

            # Mantıksal
            elif op == TokenType.VE:
                return self._is_truthy(left) and self._is_truthy(right)
            elif op == TokenType.VEYA:
                return self._is_truthy(left) or self._is_truthy(right)

            raise RuntimeError(expr.operator, f"Bilinmeyen ikili işleç: {expr.operator.lexeme}")

        elif isinstance(expr, CallExpr):
            callee = self.evaluate(expr.callee)
            arguments = [self.evaluate(arg) for arg in expr.arguments]

            if not hasattr(callee, 'call'):
                raise RuntimeError(expr.paren, f"'{callee}' çağrılabilir bir işlev değildir.")

            if len(arguments) != callee.arity():
                raise RuntimeError(expr.paren, f"Argüman sayısı uyuşmazlığı: Beklenen {callee.arity()}, Verilen {len(arguments)}")

            return callee.call(self, arguments)

        raise RuntimeError(None, f"Bilinmeyen ifade türü: {expr.__class__.__name__}")

    def _find_in_ancestor(self, env: Environment, lexeme: str) -> bool:
        curr = env
        while curr is not None:
            if lexeme in curr.values:
                return True
            curr = curr.enclosing
        return False

    def _is_truthy(self, val: Any) -> bool:
        if val is None:
            return False
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return val != 0
        if isinstance(val, (str, list)):
            return len(val) > 0
        return True

    def _format_value(self, val: Any) -> str:
        if val is None:
            return "bos"
        if isinstance(val, bool):
            return "dogru" if val else "yanlis"
        return str(val)

    def _print_output(self, text: str) -> None:
        self.output_buffer.append(text)
        self.output_callback(text)
