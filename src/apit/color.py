from enum import IntEnum
from typing import Final

PREFIX: Final = "\033[3%dm"
SUFFIX: Final = "\033[0m"


class Color(IntEnum):
    NONE = -1
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5


def to_colored_text(text: str, color: Color) -> str:
    if color == Color.NONE:
        return text
    return f"{PREFIX % color}{text}{SUFFIX}"
