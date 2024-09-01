from __future__ import annotations

import ast


def create_logical_values_node(op: ast.boolop, values: list[ast.expr], default_value: bool) -> ast.expr:
    if not values:
        return ast.Constant(value=default_value)
    if len(values) == 1:
        return values[0]
    return ast.BoolOp(op=op, values=values)


class LogicalShortCircuiting(ast.NodeTransformer):
    def visit_BoolOp(self, node: ast.BoolOp) -> ast.expr:
        if isinstance(node.op, ast.And):
            return self._visit_and(node)
        elif isinstance(node.op, ast.Or):
            return self._visit_or(node)
        return node

    def _visit_and(self, node: ast.BoolOp) -> ast.expr:
        and_values: list[ast.expr] = []
        for value in node.values:
            new_value = self.visit(value)
            if isinstance(new_value, ast.Constant):
                if new_value.value is False:
                    return new_value
                if new_value.value is True:
                    continue
            and_values.append(new_value)
        return create_logical_values_node(ast.And(), and_values, True)

    def _visit_or(self, node: ast.BoolOp) -> ast.expr:
        or_values: list[ast.expr] = []
        for value in node.values:
            new_value = self.visit(value)
            if isinstance(new_value, ast.Constant):
                if new_value.value is True:
                    return new_value
                if new_value.value is False:
                    continue
            or_values.append(new_value)
        return create_logical_values_node(ast.Or(), or_values, False)


class LogicCluster:
    def __init__(self, ids: set[int]) -> None:
        self.ids = ids
        self.subexpressions = set[str]()

    def match(self, other: LogicCluster) -> bool:
        return bool(self.ids & other.ids)

    def add_expression(self, expr: str) -> None:
        self.subexpressions.add(expr)

    def update(self, other: LogicCluster) -> None:
        self.ids.update(other.ids)
        self.subexpressions.update(other.subexpressions)

    def __repr__(self) -> str:
        return f"LogicCluster(ids={self.ids}, subexpressions={self.subexpressions})"


class RemoveSameSubExpressionInLogicalOp(ast.NodeTransformer):
    def __init__(self):
        self.and_clusters: list[LogicCluster] = []
        self.or_clusters: list[LogicCluster] = []

    @staticmethod
    def update_cluster(regisitry: list[LogicCluster], new_cluster: LogicCluster) -> LogicCluster:
        for cluster in regisitry:
            if cluster.match(new_cluster):
                cluster.update(new_cluster)
                return cluster
        regisitry.append(new_cluster)
        return new_cluster

    def visit_BoolOp(self, node: ast.BoolOp) -> ast.expr:
        if isinstance(node.op, ast.And):
            return self._visit_and(node)
        elif isinstance(node.op, ast.Or):
            return self._visit_or(node)
        return node

    def _visit_and(self, node: ast.BoolOp) -> ast.expr:
        node_id = id(node)
        cluster_ids = {id(value) for value in node.values}
        cluster = LogicCluster({*cluster_ids, node_id})
        cluster = self.update_cluster(self.and_clusters, cluster)
        transformed_values: list[ast.expr] = []
        for value in node.values:
            known_exprs = cluster.subexpressions.copy()
            transformed_value = self.visit(value)
            stringified_value = ast.unparse(transformed_value)
            if stringified_value not in known_exprs:
                cluster.add_expression(stringified_value)
                transformed_values.append(transformed_value)
        return create_logical_values_node(ast.And(), transformed_values, True)

    def _visit_or(self, node: ast.BoolOp) -> ast.expr:
        node_id = id(node)
        cluster_ids = {id(value) for value in node.values}
        cluster = LogicCluster({*cluster_ids, node_id})
        cluster = self.update_cluster(self.or_clusters, cluster)
        transformed_values: list[ast.expr] = []
        for value in node.values:
            known_exprs = cluster.subexpressions.copy()
            transformed_value = self.visit(value)
            stringified_value = ast.unparse(transformed_value)
            if stringified_value not in known_exprs:
                cluster.add_expression(stringified_value)
                transformed_values.append(transformed_value)
        return create_logical_values_node(ast.Or(), transformed_values, False)


def apply_logical_short_circuiting(expr: ast.AST) -> ast.AST:
    logical_short_circuiting = LogicalShortCircuiting()
    return logical_short_circuiting.visit(expr)


def apply_remove_same_subexpression_in_logical_op(expr: ast.AST) -> ast.AST:
    remove_same_subexpression_in_logical_op = RemoveSameSubExpressionInLogicalOp()
    res = remove_same_subexpression_in_logical_op.visit(expr)
    return res


def apply_logical_simplification(expr: ast.AST) -> ast.AST:
    expr = apply_remove_same_subexpression_in_logical_op(expr)
    expr = apply_logical_short_circuiting(expr)
    return expr
