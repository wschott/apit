from pathlib import Path

from apit.command_result import CommandResult


class Command:
    def execute(self, files: list[Path], options) -> CommandResult:
        raise NotImplementedError
