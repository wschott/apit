import logging

PREFIX = '\033[0;3%dm' # "[1;" for bold
SUFFIX = '\033[0m'
RED, GREEN, YELLOW, BLUE, MAGENTA = range(1, 6)
LEVEL_TO_COLOR_MAP = {
    logging.DEBUG: YELLOW,
    logging.INFO: GREEN,
    logging.WARNING: MAGENTA,
    logging.ERROR: RED,
    logging.CRITICAL: RED,
}

def to_colored_text(text, color):
    return (PREFIX % color) + text + SUFFIX

class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        return to_colored_text(super().format(record), LEVEL_TO_COLOR_MAP.get(record.levelno))
