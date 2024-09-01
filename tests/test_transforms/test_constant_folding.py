from __future__ import annotations

import ast

import pytest

from expr_simplifier.transforms import apply_constant_folding
from expr_simplifier.utils import loop_until_stable


@pytest.mark.parametrize(
    ["expr", "expected"],
    [
        ("1 + 1", "2"),
        ("not True", "False"),
        ("True and False or True", "True"),
        ("1 > 2", "False"),
        ("1 > 2 * a", "1 > 2 * a"),
        ("(1 > 2) * a", "False * a"),
        ("""f'Hello {"World"}!'""", "'Hello World!'"),
        ("(___x := 1) + 2 + ___x", "4"),
    ],
)
def test_constant_folding(expr: str, expected: str):
    tree = ast.parse(expr, mode="eval")
    transformed_tree = apply_constant_folding(tree)
    transformed_expr = ast.unparse(transformed_tree)
    assert transformed_expr == expected


@pytest.mark.parametrize(
    ["expr", "expected", "max_iter"],
    [
        ("(___x := 1 + 1) + ___x", "(___x := 2) + ___x", 1),
        ("(___x := 1 + 1) + ___x", "4", 2),
    ],
)
def test_constant_folding_loop_until_stable(expr: str, expected: str, max_iter: int):
    tree = ast.parse(expr, mode="eval")
    transformed_tree = loop_until_stable(tree, [apply_constant_folding], max_iter)
    transformed_expr = ast.unparse(transformed_tree)
    assert transformed_expr == expected
