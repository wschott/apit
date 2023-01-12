from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable
from pathlib import Path

from apit.command_result import CommandResult


class Command(ABC):
    @abstractmethod
    def execute(self, files: Iterable[Path], options) -> CommandResult:
        raise NotImplementedError
