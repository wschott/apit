from typing import Protocol

from apit.core.errors import ApitError
from apit.core.metadata.song import Song


class MetadataParser(Protocol):
    def extract_songs(self, metadata_json: str) -> list[Song]: ...


class ApitMetadataParsingError(ApitError):
    pass
