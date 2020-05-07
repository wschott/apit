import importlib
import logging
from pathlib import Path

from apit.debug_helper import logging_debug_filelist
from apit.error import ApitError
from apit.file_handling import get_files
from apit.logger import ColoredFormatter

FILE_FILTER = '.m4a'
LOG_PATH = '~/.apit'


def main(options):
    configure_logging(options.verbose_level)

    logging.debug('CLI options: %s', options)

    files = get_files(options.path, FILE_FILTER)
    if len(files) == 0:
        raise ApitError('No matching files found')
    logging.debug('Input path: %s', options.path)

    logging_debug_filelist('Matched files:', files)

    try:
        mod = importlib.import_module('apit.command.%s' % options.command)
        command_execute = mod.execute
    except (ImportError, AttributeError):
        raise ApitError(f'Command "{options.command}" or corresponding execute() function not found')
    else:
        options.log_path = Path(LOG_PATH).expanduser()
        command_execute(files, options)

def configure_logging(verbose_level):
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(ColoredFormatter('%(message)s'))

    VERBOSITY_TO_LOG_LEVEL_MAPPING = {
        1: logging.INFO,
        2: logging.DEBUG,
    }

    log_level = VERBOSITY_TO_LOG_LEVEL_MAPPING.get(verbose_level, logging.WARN)
    logging.basicConfig(level=log_level, handlers=[consoleHandler])
