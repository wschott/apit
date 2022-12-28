import logging
from pathlib import Path

from apit.command import Command
from apit.command_result import CommandResult
from apit.commands import determine_command_type
from apit.defaults import CACHE_PATH
from apit.defaults import FILE_FILTER
from apit.error import ApitError
from apit.file_handling import collect_files
from apit.logger import ColoredFormatter


def main(options) -> CommandResult:
    configure_logging(_to_log_level(options.verbose_level))

    logging.info("CLI options: %s", options)

    files = collect_files(options.path, FILE_FILTER)
    if not files:
        raise ApitError("No matching files found")
    logging.info("Input path: %s", options.path)

    options.cache_path = Path(CACHE_PATH).expanduser()

    CommandType: type[Command] = determine_command_type(options.command)
    return CommandType().execute(files, options)


def configure_logging(log_level: int) -> None:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter("%(levelname)s: %(message)s"))
    logging.basicConfig(level=log_level, handlers=[console_handler])


def _to_log_level(verbose_level: int) -> int:
    return {
        1: logging.INFO,
        2: logging.DEBUG,  # TODO not used anymore
    }.get(verbose_level, logging.WARN)
