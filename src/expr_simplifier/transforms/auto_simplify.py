from __future__ import annotations

import ast

from expr_simplifier.transforms.constant_folding import apply_constant_folding
from expr_simplifier.transforms.cse import apply_cse
from expr_simplifier.transforms.logical_simplification import apply_logical_simplification
from expr_simplifier.utils import loop_until_stable


def auto_simplify(expr: ast.AST) -> ast.AST:
    return loop_until_stable(expr, [apply_constant_folding, apply_logical_simplification, apply_cse], max_iter=100)
