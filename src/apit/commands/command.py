from collections.abc import Iterable
from pathlib import Path
from typing import Protocol

from apit.core.options import Options
from apit.core.result import Result


class Command(Protocol):
    @staticmethod
    def setup_cli_parser(subparsers): ...

    @staticmethod
    def execute(files: Iterable[Path], options: Options) -> Result: ...
