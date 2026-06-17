import argparse
import logging
import sys
from collections.abc import Iterable
from typing import Any, Optional

import setdoc

import normdata.json.main
from normdata.enum.Instruction import Instruction
from normdata.enum.Selector import Selector
from normdata.parsing.SuperParser import SuperParser

from .run import run

__all__ = ["main"]


@setdoc.basic
def main(args: Optional[Iterable[str]] = None, /) -> None:
    parser: SuperParser
    parser = SuperParser(
        desc="This project normalizes data in files.",
    )
    parser.add_subcommand("json")
    try:
        args_ = parser.parse_args(args)
    except ValueError as e:
        logging.error(e)
        parser.print_help(file=sys.stderr)
        sys.exit(1)
    if not args_:
        return
    subcmd = args_.pop(0)
    if subcmd == "json":
        normdata.json.main.main(args_)
    raise NotImplementedError("Unreachable code reached!")
