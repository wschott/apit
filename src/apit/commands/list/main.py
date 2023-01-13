from argparse import RawDescriptionHelpFormatter
from collections.abc import Iterable
from pathlib import Path

from ..common_cli_parser_arguments import add_path_argument
from ..common_cli_parser_arguments import add_verbose_argument
from .command import ListCommand
from apit.cli_options import CliOptions
from apit.command_result import CommandResult


def setup_cli_parser(subparsers):
    list_command = subparsers.add_parser(
        "list",
        aliases=["ls"],
        help="list metadata tags of files in PATH",
        formatter_class=RawDescriptionHelpFormatter,
        description="list metadata tags of files in PATH",
    )
    list_command.set_defaults(func=main)

    add_verbose_argument(list_command)
    add_path_argument(list_command)


def main(files: Iterable[Path], options: CliOptions) -> CommandResult:
    return ListCommand().execute(files, options)
