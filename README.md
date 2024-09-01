# Expr Simplifier

🍋‍🟩 A tool for simplifying Python expressions that don't contain side effects, mainly for generated code

<p align="center">
   <a href="https://python.org/" target="_blank"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/expr-simplifier?logo=python&style=flat-square"></a>
   <a href="https://pypi.org/project/expr-simplifier/" target="_blank"><img src="https://img.shields.io/pypi/v/expr-simplifier?style=flat-square" alt="pypi"></a>
   <a href="https://pypi.org/project/expr-simplifier/" target="_blank"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/expr-simplifier?style=flat-square"></a>
   <a href="LICENSE"><img alt="LICENSE" src="https://img.shields.io/github/license/ShigureLab/expr-simplifier?style=flat-square"></a>
   <br/>
   <a href="https://github.com/astral-sh/uv"><img alt="uv" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json&style=flat-square"></a>
   <a href="https://github.com/astral-sh/ruff"><img alt="ruff" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square"></a>
   <a href="https://gitmoji.dev"><img alt="Gitmoji" src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67?style=flat-square"></a>
</p>

## Installation

TODO...

## Usage

```console
$ expr_simplifier cse "a * 4 + (a * 4)"
(___t_0 := (a * 4)) + ___t_0
$ expr_simplifier constant_folding "(___x := 1 + 1) + ___x" --max-iter=1
(___x := 2) + ___x
$ expr_simplifier constant_folding "(___x := 1 + 1) + ___x" --max-iter=2
4
```

## TODOs

-  [ ] Fold same logic operations (`a and b and a` -> `a and b`)
-  [ ] Add runtime checks in uts
