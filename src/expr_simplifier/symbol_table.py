from __future__ import annotations


class UniqueNameGenerator:
    def __init__(self, prefix: str):
        self.prefix = prefix
        self._counter = 0

    def generate_name(self) -> str:
        name = f"{self.prefix}{self._counter}"
        self._counter += 1
        return name


class SymbolTable:
    def __init__(self):
        self._symbols = set[str]()
        self._name_generator = UniqueNameGenerator("___t_")

    def define_symbol(self, symbol: str):
        self._symbols.add(symbol)

    def request_new_symbol(self) -> str:
        while True:
            new_symbol = self._name_generator.generate_name()
            if self.is_symbol_defined(new_symbol):
                continue
            self.define_symbol(new_symbol)
            return new_symbol

    def is_symbol_defined(self, symbol: str) -> bool:
        return symbol in self._symbols

    def __contains__(self, symbol: str) -> bool:
        return self.is_symbol_defined(symbol)
