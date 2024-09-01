from __future__ import annotations

import ast
from collections.abc import Callable

from typing_extensions import TypeAlias

Pass: TypeAlias = Callable[[ast.AST], ast.AST]
