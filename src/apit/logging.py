import logging

from apit.logger import ColoredFormatter


def configure_logging(log_level: int) -> None:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter("%(levelname)s: %(message)s"))
    logging.basicConfig(level=log_level, handlers=[console_handler])
