from pathlib import Path
from typing import Protocol

from apit.cli_options import CliOptions
from apit.command_result import CommandResult


class Command(Protocol):
    @staticmethod
    def setup_cli_parser(subparsers): ...

    @staticmethod
    def execute(files: list[Path], options: CliOptions) -> CommandResult: ...
