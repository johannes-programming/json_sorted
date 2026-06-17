import sys
from collections.abc import Iterable
from typing import Optional


def getopt_long(
    args: Optional[Iterable[str]] = None,
    longopts: Iterable[str] = (),
    /,
) -> tuple[list[str], list[str]]:
    """
    POSIX-style getopt (flags only).

    Rules:
    - Parsing stops at the first positional argument.
    - "--" is treated as a positional argument (and stops parsing).
    - Short options are flags only:
        -f -x
        -fx   -> ['-f', '-x']
    - Long options are flags only:
        --foo
    - If a long option has "=value", the value is ignored:
        --foo=42 -> '--foo'
    - Abbreviated long options are expanded if unique:
        --fo -> --foo
    - Unknown long options or ambiguous abbreviations are kept as-is.
    """
    longset: set[str]
    argv: list[str]
    opts: list[str]
    possible: set[str]
    if args is None:
        argv = list(sys.argv[1:])
    else:
        argv = list(args)
    longset = set(longopts)
    opts = []
    while argv:
        if argv[0] == "--":
            argv.pop(0)
            break
        if argv[0] == "-" or not argv[0].startswith("-"):
            break
        if not argv[0].startswith("--"):
            for x in argv[0][1:]:
                opts.append(f"-{x}")
            argv.pop(0)
            continue
        opt = argv.pop(0)[2:].split("=", 1)[0]
        if opt in longset:
            opts.append(opt)
            continue
        possible = set()
        for x in longset:
            if x.startswith(opt):
                possible.add(x)
        if len(possible) == 1:
            opt = possible.pop()
        opts.append("--" + opt)
    return opts, argv
