from __future__ import annotations

import ast

from expr_simplifier.typing import Pass


def loop_until_stable(expr: ast.AST, passes: list[Pass], max_iter: int) -> ast.AST:
    for _ in range(max_iter):
        original_expr_string = ast.unparse(expr)
        for pass_ in passes:
            expr = pass_(expr)
        transformed_expr_string = ast.unparse(expr)
        if original_expr_string == transformed_expr_string:
            return expr
    return expr
