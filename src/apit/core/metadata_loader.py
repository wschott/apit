from typing import Protocol


class MetadataLoader(Protocol):
    def load(self, source: str) -> str: ...
