from argparse import ArgumentParser
from argparse import ArgumentTypeError
from pathlib import Path


def add_verbose_argument(subparser: ArgumentParser) -> None:
    subparser.add_argument(
        "-v",
        dest="verbose_level",
        action="count",
        default=0,
        help="increase verbosity of reporting (-vv prints debug messages)",
    )


def add_path_argument(subparser: ArgumentParser) -> None:
    subparser.add_argument(
        "path",
        metavar="PATH",
        type=absolute_path,
        help="path containing files",
    )


def absolute_path(path: str) -> Path:
    abs_path = Path(path).absolute()
    if not abs_path.exists():
        raise ArgumentTypeError(f"invalid path: {path}")
    return abs_path
