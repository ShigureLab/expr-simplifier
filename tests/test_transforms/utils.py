from __future__ import annotations

import ast
from typing import Any

from expr_simplifier.analyzer import analyze_external_symbols


class AnyObject:
    """A top type that can represent any object in Python"""

    def __init__(self, name: str):
        self.name = name

    def __add__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{self.name} + {other.name}")

    def __radd__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{other.name} + {self.name}")

    def __sub__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{self.name} - {other.name}")

    def __rsub__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{other.name} - {self.name}")

    def __mul__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{self.name} * {other.name}")

    def __rmul__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{other.name} * {self.name}")

    def __truediv__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{self.name} / {other.name}")

    def __rtruediv__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{other.name} / {self.name}")

    def __floordiv__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{self.name} // {other.name}")

    def __rfloordiv__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{other.name} // {self.name}")

    def __lshift__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{self.name} << {other.name}")

    def __rshift__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{self.name} >> {other.name}")

    def __or__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{self.name} | {other.name}")

    def __xor__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{other.name} ^ {self.name}")

    def __pow__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{self.name} ** {other.name}")

    def __mod__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{self.name} % {other.name}")

    def __and__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{self.name} & {other.name}")

    def __getattr__(self, name: str):
        return AnyObject(f"{self.name}.{name}")

    def __getitem__(self, key: Any):
        key = AnyObject.to_any_object(key)
        return AnyObject(f"{self.name}[{key.name}]")

    def __call__(self, *args: Any, **kwargs: Any):
        formatted_args = ", ".join(AnyObject.to_any_object(arg).name for arg in args)
        formatted_kwargs = ", ".join(f"{key}={AnyObject.to_any_object(value).name}" for key, value in kwargs.items())
        return AnyObject(f"{self.name}({formatted_args}, {formatted_kwargs})")

    def __bool__(self):
        return hash(self.name) % 2 == 0

    def __hash__(self):
        return hash(self.name)

    # def __eq__(self, other: object):
    #     other = AnyObject.to_any_object(other)
    #     return AnyObject(f"{self.name} == {other.name}")

    # def __ne__(self, other: object):
    #     other = AnyObject.to_any_object(other)
    #     return AnyObject(f"{self.name} != {other.name}")

    def __lt__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{self.name} < {other.name}")

    def __le__(self, other: Any):
        other = AnyObject.to_any_object(other)
        return AnyObject(f"{self.name} <= {other.name}")

    def __repr__(self):
        return f"AnyObject({self.name})"

    def __neg__(self):
        return AnyObject(f"-{self.name}")

    def __pos__(self):
        return AnyObject(f"+{self.name}")

    def __invert__(self):
        return AnyObject(f"~{self.name}")

    @staticmethod
    def to_any_object(value: Any):
        if isinstance(value, AnyObject):
            return value
        return AnyObject.from_raw(value)

    @staticmethod
    def from_raw(value: Any):
        return AnyObject(f"$R({value!r})")


def check_expr_at_runtime(original_ast: ast.AST, transformed_ast: ast.AST) -> None:
    original_externel_symbols = analyze_external_symbols(original_ast)
    transformed_externel_symbols = analyze_external_symbols(transformed_ast)
    assert original_externel_symbols == transformed_externel_symbols, "External symbols are different"
    original_expr = ast.unparse(original_ast)
    transformed_expr = ast.unparse(transformed_ast)
    externel_fake_values = {symbol: AnyObject(symbol) for symbol in original_externel_symbols}
    original_expr_result = eval(original_expr, externel_fake_values)
    transformed_expr_result = eval(transformed_expr, externel_fake_values)
    assert repr(original_expr_result) == repr(transformed_expr_result), "Results are different"
