from __future__ import annotations

import ast

import pytest

from expr_simplifier.transforms.method_to_operator import apply_method_to_operator

from .utils import check_expr_at_runtime


@pytest.mark.parametrize(
    ["expr", "expected"],
    [
        ("a.__add__(b)", "a + b"),
        ("a.__sub__(b)", "a - b"),
        ("a.__mul__(b)", "a * b"),
        ("a.__truediv__(b)", "a / b"),
        ("a.__floordiv__(b)", "a // b"),
        ("a.__mod__(b)", "a % b"),
        ("a.__pow__(b)", "a ** b"),
        ("a.__and__(b)", "a & b"),
        ("a.__or__(b)", "a | b"),
        ("a.__xor__(b)", "a ^ b"),
        ("a.__lshift__(b)", "a << b"),
        ("a.__rshift__(b)", "a >> b"),
        ("a.b.__add__(c.d)", "a.b + c.d"),
        ("a.__add__(b).__mul__(c)", "(a + b) * c"),
        ("a.__add__(b.__mul__(c))", "a + b * c"),
        ("a.method(b).__add__(c)", "a.method(b) + c"),
        ("a.__add__(b.method(c))", "a + b.method(c)"),
        ("a.b.c.__add__(d.e.f)", "a.b.c + d.e.f"),
        ("a.__add__(b).__sub__(c.__mul__(d))", "a + b - c * d"),
    ],
)
def test_method_to_operator(expr: str, expected: str):
    tree = ast.parse(expr, mode="eval")
    transformed_tree = apply_method_to_operator(tree)
    transformed_expr = ast.unparse(transformed_tree)
    assert transformed_expr == expected
    check_expr_at_runtime(tree, transformed_tree)


@pytest.mark.parametrize(
    ["expr", "expected"],
    [
        ("a.method(b)", "a.method(b)"),
        ("a.__unknown__(b)", "a.__unknown__(b)"),
        ("a.__add__", "a.__add__"),
    ],
)
def test_method_to_operator_no_change(expr: str, expected: str):
    tree = ast.parse(expr, mode="eval")
    transformed_tree = apply_method_to_operator(tree)
    transformed_expr = ast.unparse(transformed_tree)
    assert transformed_expr == expected
