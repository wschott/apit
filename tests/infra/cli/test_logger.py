import logging

from apit.infra.cli.color import Color
from apit.infra.cli.color import to_colored_text
from apit.infra.cli.logger import ColoredFormatter


def test_colored_formatter():
    formatter = ColoredFormatter()
    test_log_record = logging.LogRecord(
        "test", logging.ERROR, "test.py", 1, "test-msg", None, None
    )

    assert formatter.format(test_log_record) == to_colored_text("test-msg", Color.RED)
