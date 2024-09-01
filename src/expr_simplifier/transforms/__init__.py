from __future__ import annotations

from expr_simplifier.transforms.constant_folding import apply_constant_folding as apply_constant_folding
from expr_simplifier.transforms.cse import apply_cse as apply_cse
from expr_simplifier.transforms.inline_named_expr import (
    apply_constant_propagation as apply_constant_propagation,
    apply_inline_all_named_expr as apply_inline_all_named_expr,
)
from expr_simplifier.transforms.logical_simplification import (
    apply_logical_short_circuiting as apply_logical_short_circuiting,
    apply_logical_simplification as apply_logical_simplification,
    apply_remove_same_subexpression_in_logical_op as apply_remove_same_subexpression_in_logical_op,
)
from expr_simplifier.transforms.remove_unused_named_expr import (
    apply_remove_unused_named_expr as apply_remove_unused_named_expr,
)
