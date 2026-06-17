import glob
import json
import os
from collections.abc import Iterable
from typing import Any, Literal, cast

import setdoc

import normdata.json.run
from normdata.enum.Instruction import Instruction
from normdata.enum.Selector import Selector

__all__ = ["run"]


@setdoc.basic
def run(
    subCommand: Literal["json"],
    /,
    *args: str,
    **kwargs: Any,
) -> None:
    if subCommand == "json":
        normdata.json.run.run(*args, **kwargs)
    else:
        raise ValueError(f"Subcommand {subCommand!r} unknown!")
