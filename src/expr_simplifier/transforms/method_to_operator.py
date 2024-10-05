from __future__ import annotations

import ast
from ast import Add, BitAnd, BitOr, BitXor, Div, FloorDiv, Invert, LShift, Mod, Mult, Pow, RShift, Sub, UAdd, USub

MAGIC_NAMES_TO_BINARY_OPS: dict[str, ast.operator] = {
    "__add__": Add(),
    "__sub__": Sub(),
    "__mul__": Mult(),
    "__truediv__": Div(),
    "__floordiv__": FloorDiv(),
    "__mod__": Mod(),
    "__pow__": Pow(),
    "__and__": BitAnd(),
    "__or__": BitOr(),
    "__xor__": BitXor(),
    "__lshift__": LShift(),
    "__rshift__": RShift(),
}

MAGIC_NAMES_TO_REVERSE_BINARY_OPS: dict[str, ast.operator] = {
    "__radd__": Add(),
    "__rsub__": Sub(),
    "__rmul__": Mult(),
    "__rtruediv__": Div(),
    "__rfloordiv__": FloorDiv(),
    "__rmod__": Mod(),
    "__rpow__": Pow(),
    "__rand__": BitAnd(),
    "__ror__": BitOr(),
    "__rxor__": BitXor(),
    "__rlshift__": LShift(),
    "__rrshift__": RShift(),
}

MAGIC_NAMES_TO_UNARY_OPS: dict[str, ast.unaryop] = {
    "__neg__": USub(),
    "__pos__": UAdd(),
    "__invert__": Invert(),
}


class MethodToOperator(ast.NodeTransformer):
    def visit_Call(self, node: ast.Call) -> ast.AST:
        if not isinstance(node.func, ast.Attribute):
            return self.generic_visit(node)
        if node.func.attr in MAGIC_NAMES_TO_BINARY_OPS and len(node.args) == 1:
            return ast.BinOp(
                left=MethodToOperator().visit(node.func.value),
                op=MAGIC_NAMES_TO_BINARY_OPS[node.func.attr],
                right=MethodToOperator().visit(node.args[0]),
            )
        if node.func.attr in MAGIC_NAMES_TO_REVERSE_BINARY_OPS and len(node.args) == 1:
            return ast.BinOp(
                left=MethodToOperator().visit(node.args[0]),
                op=MAGIC_NAMES_TO_REVERSE_BINARY_OPS[node.func.attr],
                right=MethodToOperator().visit(node.func.value),
            )
        if node.func.attr in MAGIC_NAMES_TO_UNARY_OPS and len(node.args) == 0:
            return ast.UnaryOp(
                op=MAGIC_NAMES_TO_UNARY_OPS[node.func.attr],
                operand=MethodToOperator().visit(node.func.value),
            )
        return self.generic_visit(node)


def apply_method_to_operator(expr: ast.AST) -> ast.AST:
    return MethodToOperator().visit(expr)
