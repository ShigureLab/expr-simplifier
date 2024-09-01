from __future__ import annotations

import ast

from expr_simplifier import auto_simplify

code = "a[1 + 1].b + a[3 - 1].b.c + (___x := 2) + (a[2].b and (___x == 2) and a[2].b)"
tree = ast.parse(code, mode="eval")
simplified_tree = auto_simplify(tree)
print(ast.unparse(simplified_tree))
# (___t_1 := a[2].b) + ___t_1.c + 2 + ___t_1
