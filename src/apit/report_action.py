from abc import ABC
from abc import abstractmethod


class ActionReporter(ABC):
    @property
    @abstractmethod
    def preview_msg(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def status_msg(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def result(self) -> str:
        raise NotImplementedError
