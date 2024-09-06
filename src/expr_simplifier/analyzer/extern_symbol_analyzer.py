from __future__ import annotations

import ast

from expr_simplifier.symbol_table import SymbolTable


class ExternalSymbolAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.external_symbols: list[str] = []

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Store):
            self.symbol_table.define_symbol(node.id)
        elif isinstance(node.ctx, ast.Load):
            if not self.symbol_table.is_symbol_defined(node.id) and node.id not in self.external_symbols:
                self.external_symbols.append(node.id)


def analyze_external_symbols(tree: ast.AST) -> list[str]:
    analyzer = ExternalSymbolAnalyzer()
    analyzer.visit(tree)
    return analyzer.external_symbols
