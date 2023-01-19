from abc import ABC
from abc import abstractmethod
from pathlib import Path

from apit.file_tags import FileTags
from apit.metadata import Artwork
from apit.metadata import Song


class Format(ABC):
    extensions: list[str] = []

    @staticmethod
    @abstractmethod
    def read(file: Path) -> FileTags:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def update(file: Path, song: Song, artwork: Artwork | None = None) -> FileTags:
        raise NotImplementedError
