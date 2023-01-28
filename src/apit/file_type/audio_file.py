from pathlib import Path
from typing import Protocol

from apit.factory import Factory
from apit.file_tags import FileTags
from apit.metadata import Artwork
from apit.metadata import Song


class AudioFile(Protocol):
    def __init__(self, file: Path) -> None:
        ...

    def read(self) -> FileTags:
        ...

    def update(self, song: Song, artwork: Artwork | None = None) -> FileTags:
        ...


class AudioFileFactory(Factory[AudioFile]):
    @classmethod
    def load(cls, file: Path) -> AudioFile:
        return super().create(file.suffix[1:], file)

    @classmethod
    def get_supported_extensions(cls) -> list[str]:
        return super().get_factory_types()
