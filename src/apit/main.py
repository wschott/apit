import logging
from pathlib import Path
from typing import Type

from apit.command import Command
from apit.commands import determine_command_type
from apit.defaults import CACHE_PATH, FILE_FILTER
from apit.error import ApitError
from apit.file_handling import collect_files
from apit.logger import ColoredFormatter


def main(options) -> int:
    configure_logging(options.verbose_level)

    logging.info('CLI options: %s', options)

    files = collect_files(options.path, FILE_FILTER)
    if len(files) == 0:
        raise ApitError('No matching files found')
    logging.info('Input path: %s', options.path)

    options.cache_path = Path(CACHE_PATH).expanduser()

    CommandType: Type[Command] = determine_command_type(options.command)
    return CommandType().execute(files, options)


def configure_logging(verbose_level: int) -> None:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter('%(levelname)s: %(message)s'))

    VERBOSITY_TO_LOG_LEVEL_MAPPING = {
        1: logging.INFO,
        2: logging.DEBUG,  # TODO not used anymore
    }

    log_level = VERBOSITY_TO_LOG_LEVEL_MAPPING.get(verbose_level, logging.WARN)
    logging.basicConfig(level=log_level, handlers=[console_handler])
