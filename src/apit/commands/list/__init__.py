from collections.abc import Iterable
from pathlib import Path
from typing import override

from .command import execute
from apit.cli_options import CliOptions
from apit.command_result import CommandResult
from apit.commands.command import Command
from apit.commands.common_cli_parser_arguments import add_path_argument
from apit.commands.common_cli_parser_arguments import add_verbose_argument

__all__ = ["ListCommand"]


class ListCommand(Command):
    @staticmethod
    @override
    def setup_cli_parser(subparsers):
        list_command = subparsers.add_parser(
            "list",
            aliases=["ls"],
            help="list metadata tags of files in PATH",
            description="list metadata tags of files in PATH",
        )
        list_command.set_defaults(func=ListCommand.execute)

        add_verbose_argument(list_command)
        add_path_argument(list_command)

    @staticmethod
    @override
    def execute(files: Iterable[Path], options: CliOptions) -> CommandResult:
        return execute(files=files, verbose_level=options.verbose_level)
