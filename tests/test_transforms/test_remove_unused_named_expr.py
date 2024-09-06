from __future__ import annotations

import ast

import pytest

from expr_simplifier.transforms import apply_remove_unused_named_expr

from .utils import check_expr_at_runtime


@pytest.mark.parametrize(
    ["expr", "expected"],
    [
        ("(___x := a.b) + ___x", "(___x := a.b) + ___x"),
        ("(___y := (___x := a.b)) + ___y", "(___y := a.b) + ___y"),
        ("(___y := (___x := a.b))", "a.b"),
    ],
)
def test_inline_named_expr(expr: str, expected: str):
    tree = ast.parse(expr, mode="eval")
    transformed_tree = apply_remove_unused_named_expr(tree)
    transformed_expr = ast.unparse(transformed_tree)
    assert transformed_expr == expected
    check_expr_at_runtime(tree, transformed_tree)
