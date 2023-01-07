from abc import ABC
from abc import abstractmethod
from typing import Any

from apit.tag_id import TagId


class TagIdDescriptionValue(ABC):
    def __init__(self, tag_id: TagId, value: Any) -> None:
        self.tag_id: TagId = tag_id
        self._unprocessed_value: Any = value

    def __eq__(self, other) -> bool:
        if isinstance(other, TagId):
            return self.tag_id == other
        return False

    def description(self, verbose: bool) -> str:
        if description := self._get_human_readable_description(self.tag_id):
            return f"{description} ({self.tag_id})" if verbose else description
        return self.tag_id

    @abstractmethod
    def _get_human_readable_description(self, tag_id: TagId) -> str | None:
        return NotImplemented

    @abstractmethod
    def value(self, verbose: bool) -> str:
        return NotImplemented
