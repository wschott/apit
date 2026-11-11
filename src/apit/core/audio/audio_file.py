from pathlib import Path
from typing import Protocol

from apit.core.audio.file_tags import FileTags
from apit.core.metadata.artwork import Artwork
from apit.core.metadata.song import Song


class AudioFile(Protocol):
    def __init__(self, file: Path) -> None: ...

    def read(self) -> FileTags: ...

    def update(self, song: Song, artwork: Artwork | None = None) -> FileTags: ...
