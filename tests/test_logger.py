import logging

from apit.logger import ColoredFormatter
from apit.report import Color, to_colored_text


def test_colored_formatter():
    formatter = ColoredFormatter()
    test_log_record = logging.LogRecord(None, logging.ERROR, None, None, 'test-msg', None, None)

    assert formatter.format(test_log_record) == to_colored_text('test-msg', Color.RED)
