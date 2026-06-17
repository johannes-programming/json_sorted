import logging
import sys
from collections.abc import Generator, Iterable
from typing import Any, Optional, Self

from .getopt_long import getopt_long

__all__ = ["SuperParser"]

NO_SUBCOMMAND = "Required subcommand absent!"
UNKNOWN_SUBCOMMAND = "Subcommand unknown!"
UNKNOWN_OPTION = "Option unknown!"
HELP_FLAGS = "-h, --help"
HELP_DESC = "show this help message and exit"


class SubCommand:
    def __init__(
        self: Self,
        name: str,
        *,
        desc: Optional[str] = None,
        aliases: Iterable[str] = (),
    ) -> None:
        self.name = name
        self.desc = desc
        self.aliases = tuple(aliases)

    def get_help_pair(self: Self) -> tuple[str, str]:
        ans: str
        ans = self.name
        if self.aliases:
            ans += f" ({','.join(self.aliases)})"
        return ans, self.desc or ""


class SuperParser:

    def __init__(
        self: Self,
        prog: Optional[str] = None,
        *,
        desc: Optional[str] = None,
        # version: Optional[str] = None,
    ) -> None:
        if prog is None:
            prog = sys.argv[0]
        self.prog = prog
        self.desc = desc
        self.subCommands: list[SubCommand] = list()
        # self.version = version

    def add_subcommand(
        self: Self,
        name: str,
        *,
        desc: Optional[str] = None,
        aliases: Iterable[str] = (),
    ) -> None:
        self.subCommands.append(SubCommand(name, desc=desc, aliases=aliases))

    def gen_help(self: Self) -> Generator[str, None, None]:
        if self.desc is not None:
            yield self.desc
            yield ""
        yield self.get_usage()
        yield ""
        yield "possible subcommands:"
        help_pairs = [cmd.get_help_pair() for cmd in self.subCommands]
        shift = 0
        for x, y in help_pairs:
            shift = max(shift, len(x))
        shift = max(shift, len(HELP_FLAGS))
        shift += 2
        for x, y in help_pairs:
            yield f"  {x:<{shift}}{y}"
        yield ""
        yield "options:"
        yield f"  {HELP_FLAGS:<{shift}}{HELP_DESC}"

    def get_usage(self: Self) -> str:
        ans: str
        values: list[str]
        values = list()
        for cmd in self.subCommands:
            values.append(cmd.name)
            values.extend(cmd.aliases)
        return "usage: {0} [-h] {1} ...".format(self.prog, ",".join(values))

    def parse_args(
        self: Self, args: Optional[Iterable[str]] = None, /
    ) -> list[str]:
        opts, args_ = getopt_long(args, ["help"])
        if set(opts).intersection({"-h", "--help"}):
            self.print_help()
            return []
        if opts:
            raise ValueError(UNKNOWN_OPTION)
        if not args_:
            raise ValueError(NO_SUBCOMMAND)
        for cmd in self.subCommands:
            if args_[0] == cmd.name:
                return args_
        for cmd in self.subCommands:
            if args_[0] in cmd.aliases:
                args_[0] = cmd.name
                return args_
        raise ValueError(UNKNOWN_SUBCOMMAND)

    def print_help(self: Self, **kwargs: Any) -> None:
        for line in self.gen_help():
            print(line, **kwargs)
