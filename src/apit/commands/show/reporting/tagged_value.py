from abc import ABC
from abc import abstractmethod
from typing import Any

from apit.commands.show.reporting.readable_names import ReadableTagName
from apit.tag_id import TagId


class TaggedValue(ABC):
    def __init__(self, tag_id: TagId, value: Any) -> None:
        self.tag_id: TagId = tag_id
        self.readable_name: ReadableTagName | None = self._get_readable_name(
            self.tag_id
        )
        self._unprocessed_value: Any = value

    def __eq__(self, other) -> bool:
        if isinstance(other, TaggedValue):
            return (
                self.tag_id == other.tag_id
                and self._unprocessed_value == other._unprocessed_value
            )
        return False

    def description(self, verbose: bool) -> str:
        if not self.readable_name:
            return self.tag_id

        if verbose:
            return f"{self.readable_name} ({self.tag_id})"
        else:
            return self.readable_name

    @property
    def is_known(self) -> bool:
        return self.readable_name is not None

    @abstractmethod
    def _get_readable_name(self, tag_id: TagId) -> ReadableTagName | None:
        return NotImplemented

    @abstractmethod
    def value(self, verbose: bool) -> str:
        return NotImplemented
