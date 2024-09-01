from __future__ import annotations

import ast

import pytest

from expr_simplifier.transforms import apply_inline_named_expr


@pytest.mark.parametrize(
    ["expr", "expected"],
    [
        ("(___x := a.b)", "a.b"),
        ("(___x := a.b).c", "a.b.c"),
        ("(___x := a.b).c + ___x.d.e", "a.b.c + a.b.d.e"),
        ("(___y := (___x := a.b)).c + ___x.d.e", "a.b.c + a.b.d.e"),
        ("(___y := (___x := a.b).c) + ___x.d.e + ___y.f.g", "a.b.c + a.b.d.e + a.b.c.f.g"),
    ],
)
def test_inline_named_expr(expr: str, expected: str):
    tree = ast.parse(expr, mode="eval")
    transformed_tree = apply_inline_named_expr(tree)
    transformed_expr = ast.unparse(transformed_tree)
    assert transformed_expr == expected


@pytest.mark.parametrize(
    ["expr", "expected"],
    [
        ("(___x := a.b)", "(___x := a.b)"),
        ("(___x := a.b).c", "(___x := a.b).c"),
        ("(___x := a.b).c + ___x.d.e", "(___x := a.b).c + ___x.d.e"),
        ("(___x := 1) + ___x", "1 + 1"),
        ("(___y := (___x := 1)) + ___x + ___y", "1 + 1 + 1"),
        ("(___x := 1 + 1) + ___x", "(___x := (1 + 1)) + ___x"),
    ],
)
def test_constant_propagation(expr: str, expected: str):
    tree = ast.parse(expr, mode="eval")
    transformed_tree = apply_inline_named_expr(tree, constant_only=True)
    transformed_expr = ast.unparse(transformed_tree)
    assert transformed_expr == expected
