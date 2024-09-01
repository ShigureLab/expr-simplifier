from __future__ import annotations

import ast


class UsedSymbolsAnalyzer(ast.NodeVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.used_symbols = set[str]()

    def visit_Name(self, node: ast.Name) -> None:
        symbol = node.id
        if isinstance(node.ctx, ast.Load):
            self.used_symbols.add(symbol)


class RemoveUnusedNamedExpr(ast.NodeTransformer):
    def __init__(self, used_symbols: set[str]) -> None:
        super().__init__()
        self.used_symbols = used_symbols

    def visit_NamedExpr(self, node: ast.NamedExpr) -> ast.expr:
        value = self.visit(node.value)
        name = node.target.id
        if name not in self.used_symbols:
            return value
        return node


def apply_remove_unused_named_expr(expr: ast.AST) -> ast.AST:
    used_symbols_analyzer = UsedSymbolsAnalyzer()
    used_symbols_analyzer.visit(expr)
    used_symbols = used_symbols_analyzer.used_symbols

    remove_unused_named_expr = RemoveUnusedNamedExpr(used_symbols)
    return remove_unused_named_expr.visit(expr)
