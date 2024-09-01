from __future__ import annotations

import ast

import pytest

from expr_simplifier.transforms import apply_cse


@pytest.mark.parametrize(
    ["expr", "expected"],
    [
        ("a + a", "a + a"),
        ("(a + b) + (a + b)", "(___t_0 := (a + b)) + ___t_0"),
        ("(___x := (a + b)) + ___x", "(___t_0 := (a + b)) + ___t_0"),
        ("(___t_0 := (a + b)) + ___t_0", "(___t_0 := (a + b)) + ___t_0"),
        ("(___t_1 := (a + b)) + ___t_1", "(___t_0 := (a + b)) + ___t_0"),
        ("a.b.c + a.b.d * a.d.e / a.d.f", "(___t_0 := a.b).c + ___t_0.d * (___t_3 := a.d).e / ___t_3.f"),
        ("1 + 1 + 2", "1 + 1 + 2"),
        (
            "(___x := a.b).c + ___x.d.e + (___y := (___z := a.b).c) + ___z.d.e + ___y.f.g",
            "(___t_1 := (___t_0 := a.b).c) + (___t_3 := (___t_2 := ___t_0.d).e) + ___t_1 + ___t_3 + ___t_1.f.g",
        ),
        (
            "a.b.c and (fn1(fn2((___x := a.b.c.d.e.f.g)))) and (___x == False) and (___y := a.b.c)",
            "(___t_1 := (___t_0 := a.b).c) and fn1(fn2((___t_5 := (___t_4 := (___t_3 := (___t_2 := ___t_1.d).e).f).g))) and (___t_5 == False) and ___t_1",
        ),
        (
            "(___x := a.b.c) + ___x",
            "(___t_1 := (___t_0 := a.b).c) + ___t_1",
        ),
    ],
)
def test_cse(expr: str, expected: str):
    tree = ast.parse(expr, mode="eval")
    transformed_tree = apply_cse(tree)
    transformed_expr = ast.unparse(transformed_tree)
    assert transformed_expr == expected
