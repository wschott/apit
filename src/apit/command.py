from collections.abc import Sequence
from pathlib import Path

from apit.command_result import CommandResult


class Command:
    def execute(self, files: Sequence[Path], options) -> CommandResult:
        raise NotImplementedError
