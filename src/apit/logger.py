import logging

from apit.color import Color
from apit.color import to_colored_text

LEVEL_TO_COLOR_MAP = {
    logging.DEBUG: Color.MAGENTA,
    logging.INFO: Color.MAGENTA,
    logging.WARNING: Color.MAGENTA,
    logging.ERROR: Color.RED,
    logging.CRITICAL: Color.RED,
}


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return to_colored_text(
            super().format(record), LEVEL_TO_COLOR_MAP.get(record.levelno, Color.NONE)
        )
