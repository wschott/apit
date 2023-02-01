from rich.console import Console

from apit.str_enum import StrEnum


class Color(StrEnum):
    GREEN = "bright_green"
    RED = "bright_red"
    YELLOW = "bright_yellow"
    BLACK = "black"

    def bb(self) -> str:
        return f"[{self.value}]"

    def black_on(self) -> str:
        return f"[{Color.BLACK} on {self.value}]"


class Icon(StrEnum):
    OK = ":heavy_check_mark:"
    ERROR = ":heavy_multiplication_x:"


console = Console(highlight=False)
