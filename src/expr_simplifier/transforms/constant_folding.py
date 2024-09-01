from __future__ import annotations

import ast

from typing_extensions import TypeAlias

from expr_simplifier.transforms.inline_named_expr import apply_constant_propagation

SubExpressionTable: TypeAlias = dict[str, tuple[str, int]]


def fold_to_constant(node: ast.AST) -> ast.Constant:
    return ast.Constant(value=eval(ast.unparse(node)))


class ConstantFolding(ast.NodeTransformer):
    def visit(self, node: ast.AST) -> ast.AST:
        transformed_node = self.generic_visit(node)
        if isinstance(node, ast.BinOp) and isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
            return fold_to_constant(node)
        if isinstance(node, ast.UnaryOp) and isinstance(node.operand, ast.Constant):
            return fold_to_constant(node)
        if isinstance(node, ast.BoolOp) and all(isinstance(value, ast.Constant) for value in node.values):
            return fold_to_constant(node)
        if isinstance(node, ast.Compare) and all(isinstance(comp, ast.Constant) for comp in node.comparators):
            return fold_to_constant(node)
        if isinstance(node, ast.JoinedStr) and all(
            isinstance(value, ast.Constant)
            or (isinstance(value, ast.FormattedValue) and isinstance(value.value, ast.Constant))
            for value in node.values
        ):
            return fold_to_constant(node)
        return transformed_node


def apply_constant_folding(expr: ast.AST) -> ast.AST:
    # Constant propagation
    expr = apply_constant_propagation(expr)
    # Constant folding
    expr = ConstantFolding().visit(expr)
    return expr
