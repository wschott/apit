from collections.abc import Iterable
from pathlib import Path

from .command import ShowCommand
from apit.cli_options import CliOptions
from apit.command_result import CommandResult


def main(files: Iterable[Path], options: CliOptions) -> CommandResult:
    return ShowCommand().execute(files, options)
