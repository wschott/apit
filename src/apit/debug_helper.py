import logging
from pathlib import Path
from typing import List


def logging_debug_filelist(description: str, files: List[Path]):
    logging.debug(description)
    for f in files:
        logging.debug('  %s', f.name)
