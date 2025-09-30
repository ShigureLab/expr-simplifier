from __future__ import annotations

import ast
import copy
from collections.abc import Callable
from typing import TypeAlias

NamedExpressions: TypeAlias = dict[str, ast.expr]
ShouldReplaceFn: TypeAlias = Callable[[str, NamedExpressions], bool]


class InlineNamedExpr(ast.NodeTransformer):
    def __init__(self, should_replace_fn: ShouldReplaceFn) -> None:
        super().__init__()
        self.should_replace_fn = should_replace_fn
        self.named_expressions = dict[str, ast.expr]()

    def visit_NamedExpr(self, node: ast.NamedExpr) -> ast.expr:
        value = self.visit(node.value)
        name = node.target.id
        self.named_expressions[name] = value
        if not self.should_replace_fn(name, self.named_expressions):
            return node
        return value

    def visit_Name(self, node: ast.Name) -> ast.expr:
        if node.id in self.named_expressions:
            if not self.should_replace_fn(node.id, self.named_expressions):
                return node
            return copy.deepcopy(self.named_expressions[node.id])
        return node


def apply_inline_all_named_expr(expr: ast.AST) -> ast.AST:
    inline_named_expr = InlineNamedExpr(lambda symbol, named_expressions: True)
    return inline_named_expr.visit(expr)


def apply_constant_propagation(expr: ast.AST) -> ast.AST:
    inline_named_expr = InlineNamedExpr(
        lambda symbol, named_expressions: isinstance(named_expressions[symbol], ast.Constant)
    )
    return inline_named_expr.visit(expr)
