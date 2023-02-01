from apit.color import Color
from apit.color import to_colored_text


def test_to_colored_text_no_color():
    assert to_colored_text("test", Color.NONE) == "test"


def test_to_colored_text_color():
    assert to_colored_text("test", Color.RED) == "\033[31mtest\033[0m"
