from __future__ import annotations

from enum import StrEnum

from rich.console import Console


class Color(StrEnum):
    GREEN = "green"
    RED = "red"
    YELLOW = "yellow"
    BLACK = "black"
    BRIGHT_GREEN = "bright_green"
    BRIGHT_RED = "bright_red"
    BRIGHT_YELLOW = "bright_yellow"

    def as_bright(self) -> Color:
        return Color[f"BRIGHT_{str(self.name)}"]  # noqa: RUF010

    def bb(self) -> str:
        return f"[{self.value}]"

    def black_on(self) -> str:
        return f"[{Color.BLACK} on {self.value}]"


class Icon(StrEnum):
    OK = ":heavy_check_mark:"
    ERROR = ":heavy_multiplication_x:"


console = Console(highlight=False)
