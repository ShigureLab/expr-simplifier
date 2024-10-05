from __future__ import annotations

import ast
from ast import Add, BitAnd, BitOr, BitXor, Div, FloorDiv, LShift, Mod, Mult, Pow, RShift, Sub

operators: dict[str, ast.operator] = {
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


class MethodToOperator(ast.NodeTransformer):
    def visit_Call(self, node: ast.Call) -> ast.AST:
        if isinstance(node.func, ast.Attribute) and node.func.attr in operators and len(node.args) == 1:
            return ast.BinOp(
                left=MethodToOperator().visit(node.func.value),
                op=operators[node.func.attr],
                right=MethodToOperator().visit(node.args[0]),
            )
        return self.generic_visit(node)


def apply_method_to_operator(expr: ast.AST) -> ast.AST:
    return MethodToOperator().visit(expr)
