from pathlib import Path
from typing import Protocol

from apit.file_tags import FileTags
from apit.metadata import Artwork
from apit.metadata import Song


class AudioFile(Protocol):
    def __init__(self, file: Path) -> None: ...

    def read(self) -> FileTags: ...

    def update(self, song: Song, artwork: Artwork | None = None) -> FileTags: ...
