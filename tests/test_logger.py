import logging

from apit.color import Color
from apit.color import to_colored_text
from apit.logger import ColoredFormatter


def test_colored_formatter():
    formatter = ColoredFormatter()
    test_log_record = logging.LogRecord(
        None, logging.ERROR, None, None, "test-msg", None, None
    )

    assert formatter.format(test_log_record) == to_colored_text("test-msg", Color.RED)
