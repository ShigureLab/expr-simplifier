from __future__ import annotations

import ast
import copy


class InlineNamedExpr(ast.NodeTransformer):
    def __init__(self, constant_only: bool = False) -> None:
        super().__init__()
        self.named_expressions = dict[str, ast.expr]()
        self.constant_only = constant_only

    def should_replace(self, symbol: str) -> bool:
        return not self.constant_only or isinstance(self.named_expressions[symbol], ast.Constant)

    def visit_NamedExpr(self, node: ast.NamedExpr) -> ast.expr:
        value = self.visit(node.value)
        name = node.target.id
        self.named_expressions[name] = value
        if not self.should_replace(name):
            return node
        return value

    def visit_Name(self, node: ast.Name) -> ast.expr:
        if node.id in self.named_expressions:
            if not self.should_replace(node.id):
                return node
            return copy.deepcopy(self.named_expressions[node.id])
        return node


def apply_inline_named_expr(expr: ast.AST, constant_only: bool = False) -> ast.AST:
    inline_named_expr = InlineNamedExpr(constant_only)
    return inline_named_expr.visit(expr)
