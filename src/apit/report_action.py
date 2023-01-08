from abc import ABC
from abc import abstractmethod


class ActionReporter(ABC):
    @property
    @abstractmethod
    def not_actionable_msg(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def preview_msg(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def status_msg(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def result(self) -> str:
        return NotImplemented
