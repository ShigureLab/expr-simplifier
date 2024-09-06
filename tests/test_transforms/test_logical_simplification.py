from __future__ import annotations

import ast

import pytest

from expr_simplifier.transforms import (
    apply_logical_short_circuiting,
    apply_logical_simplification,
    apply_remove_same_subexpression_in_logical_op,
)

from .utils import check_expr_at_runtime


@pytest.mark.parametrize(
    ["expr", "expected"],
    [
        ("a and False and b", "False"),
        ("(a and False) and b", "False"),
        ("a and (False and b)", "False"),
        ("a or True or b", "True"),
        ("(a or True) or b", "True"),
        ("a or (True or b)", "True"),
        ("a and True and b", "a and b"),
        ("a or False or b", "a or b"),
        ("a and True or b", "a or b"),
        ("not (a and False)", "not False"),
        ("True and True", "True"),
        ("True or True", "True"),
        ("False and False", "False"),
        ("False or False", "False"),
    ],
)
def test_logical_short_circuiting(expr: str, expected: str):
    tree = ast.parse(expr, mode="eval")
    transformed_tree = apply_logical_short_circuiting(tree)
    transformed_expr = ast.unparse(transformed_tree)
    assert transformed_expr == expected
    check_expr_at_runtime(tree, transformed_tree)


@pytest.mark.parametrize(
    ["expr", "expected"],
    [
        ("a and b and a", "a and b"),
        ("(a and b) and a", "a and b"),
        ("a and (b and a)", "a and b"),
        ("a and b and a and b", "a and b"),
        ("(a and b) and (a and b)", "(a and b) and True"),
        ("a or b or a", "a or b"),
        ("(a or b) or a", "a or b"),
        ("a or (b or a)", "a or b"),
        ("a or b or a or b", "a or b"),
        ("(a or b) or (a or b)", "(a or b) or False"),
        ("a and b and c and a and b and c", "a and b and c"),
        ("(a and b) and (c and a) and b and c", "(a and b) and c"),
        ("a and (b and c) and a and b and c", "a and (b and c)"),
    ],
)
def test_remove_same_subexpression_in_logical_op(expr: str, expected: str):
    tree = ast.parse(expr, mode="eval")
    transformed_tree = apply_remove_same_subexpression_in_logical_op(tree)
    transformed_expr = ast.unparse(transformed_tree)
    assert transformed_expr == expected
    check_expr_at_runtime(tree, transformed_tree)


@pytest.mark.parametrize(
    ["expr", "expected"],
    [
        ("(a and b) and (a and b)", "a and b"),
        ("(a or b) or (a or b)", "a or b"),
    ],
)
def test_logical_simplification(expr: str, expected: str):
    tree = ast.parse(expr, mode="eval")
    transformed_tree = apply_logical_simplification(tree)
    transformed_expr = ast.unparse(transformed_tree)
    assert transformed_expr == expected
    check_expr_at_runtime(tree, transformed_tree)
