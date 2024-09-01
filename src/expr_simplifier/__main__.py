from __future__ import annotations

import argparse
import ast
from collections.abc import Callable

from expr_simplifier import __version__
from expr_simplifier.transforms import apply_constant_folding, apply_cse, apply_logical_simplification
from expr_simplifier.typing import Pass
from expr_simplifier.utils import loop_until_stable


def create_pass_command(name: str, passes: list[Pass]) -> Callable[[argparse.Namespace], None]:
    def pass_command(args: argparse.Namespace) -> None:
        expr = ast.parse(args.input, mode="eval")
        simplified_expr = loop_until_stable(expr, passes, args.max_iter)
        print(ast.unparse(simplified_expr))

    pass_command.__name__ = name
    return pass_command


def create_pass_parser(
    name: str,
    passes: list[Pass],
    description: str,
    subparser: argparse._SubParsersAction[argparse.ArgumentParser],  # pyright: ignore [reportPrivateUsage]
) -> None:
    parser = subparser.add_parser(name, help=description)
    parser.add_argument("input", help="The expression to simplify")
    parser.add_argument("--max-iter", type=int, default=100, help="The maximum number of iterations")
    parser.set_defaults(func=create_pass_command(name, passes))


def main() -> None:
    parser = argparse.ArgumentParser(prog="moelib", description="A moe moe project")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    sub_parsers = parser.add_subparsers(help="sub-command help", dest="sub_command")

    create_pass_parser("cse", [apply_cse], "Common Subexpression Elimination", sub_parsers)
    create_pass_parser("constant_folding", [apply_constant_folding], "Constant Folding", sub_parsers)
    create_pass_parser("logical_simplification", [apply_logical_simplification], "Logical Simplification", sub_parsers)
    create_pass_parser(
        "auto", [apply_constant_folding, apply_logical_simplification, apply_cse], "Auto Simplification", sub_parsers
    )

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
