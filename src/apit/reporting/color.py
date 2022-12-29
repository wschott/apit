from enum import Enum


PREFIX = "\033[3%dm"
SUFFIX = "\033[0m"


class Color(Enum):
    NONE = -1
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5


def to_colored_text(text: str, color: Color) -> str:
    if color == Color.NONE:
        return text
    return f"{PREFIX % color.value}{text}{SUFFIX}"
