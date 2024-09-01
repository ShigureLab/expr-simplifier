from __future__ import annotations

import ast

from typing_extensions import TypeAlias

from expr_simplifier.symbol_table import SymbolTable
from expr_simplifier.transforms.inline_named_expr import apply_inline_all_named_expr
from expr_simplifier.transforms.remove_unused_named_expr import apply_remove_unused_named_expr

SubExpressionTable: TypeAlias = dict[str, tuple[str, int]]


class CSEPreAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.subexpressions: SubExpressionTable = {}
        self.symbols = SymbolTable()
        super().__init__()

    def visit(self, node: ast.AST) -> None:
        self.generic_visit(node)
        expr_string = ast.unparse(node)
        if isinstance(node, ast.expr):
            if isinstance(node, ast.Name):
                self.symbols.define_symbol(node.id)
                return
            if isinstance(node, ast.Constant):
                return
            if expr_string not in self.subexpressions:
                self.subexpressions[expr_string] = (self.symbols.request_new_symbol(), 0)
            symbol, count = self.subexpressions[expr_string]
            self.subexpressions[expr_string] = (symbol, count + 1)


class CommonSubexpressionElimination(ast.NodeTransformer):
    def __init__(self, subexpressions: dict[str, tuple[str, int]]):
        self.subexpressions = subexpressions
        self.declared_symbols = set[str]()
        super().__init__()

    def visit(self, node: ast.AST) -> ast.AST:
        expr_string = ast.unparse(node)
        transformed_node = self.generic_visit(node)
        if isinstance(transformed_node, ast.expr) and expr_string in self.subexpressions:
            symbol, count = self.subexpressions[expr_string]
            if count > 1:
                if symbol not in self.declared_symbols:
                    self.declared_symbols.add(symbol)
                    assign_node = ast.NamedExpr(target=ast.Name(id=symbol, ctx=ast.Store()), value=transformed_node)
                    return assign_node
                return ast.Name(id=symbol, ctx=ast.Load())
        return transformed_node


def show_subexpressions(subexpressions: SubExpressionTable) -> None:
    for subexpression, (symbol, count) in subexpressions.items():
        print(f"{symbol}: {subexpression} ({count})")


def apply_cse(expr: ast.AST) -> ast.AST:
    expr = apply_inline_all_named_expr(expr)
    cse_pre_analyzer = CSEPreAnalyzer()
    cse_pre_analyzer.visit(expr)
    cse = CommonSubexpressionElimination(cse_pre_analyzer.subexpressions)
    expr = cse.visit(expr)
    return apply_remove_unused_named_expr(expr)
