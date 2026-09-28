from __future__ import annotations

import subprocess
import sys

import pytest


@pytest.mark.parametrize(
    ["args", "expected"],
    [
        (["cse", "a * 4 + (a * 4)"], "(___t_0 := (a * 4)) + ___t_0"),
        (["constant_folding", "(___x := 1 + 1) + ___x", "--max-iter=1"], "(___x := 2) + ___x"),
        (["constant_folding", "(___x := 1 + 1) + ___x", "--max-iter=2"], "4"),
        (["logical_simplification", "a and b and a"], "a and b"),
        (["auto", "1 + 1"], "2"),
    ],
)
def test_cli(args: list[str], expected: str) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "expr_simplifier", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == expected
    assert result.stderr == ""
