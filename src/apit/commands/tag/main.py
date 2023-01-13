from collections.abc import Iterable
from pathlib import Path

from .command import TagCommand
from apit.cli_options import CliOptions
from apit.command_result import CommandResult
from apit.defaults import CACHE_PATH


def main(files: Iterable[Path], options: CliOptions) -> CommandResult:
    # TODO add to CommandOptions (similar to CliOptions)?
    options.cache_path = Path(CACHE_PATH).expanduser()

    return TagCommand().execute(files, options)
