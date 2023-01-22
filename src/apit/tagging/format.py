from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path

from apit.error import ApitUnsupportedFileTypeError
from apit.file_tags import FileTags
from apit.list_utils import flatten
from apit.metadata import Artwork
from apit.metadata import Song
from apit.registry_mixin import RegistryMixin


class Format(ABC, RegistryMixin):
    extensions: list[str] = []

    @classmethod
    def from_(cls, file: Path) -> Format:
        extension = file.suffix[1:]
        for format in cls.registry:
            if extension in format.extensions:
                return format(file)
        raise ApitUnsupportedFileTypeError(extension)

    @classmethod
    def get_supported_extensions(cls) -> list[str]:
        return flatten([format.extensions for format in cls.registry])

    def __init__(self, file: Path) -> None:
        self.file: Path = file

    @abstractmethod
    def read(self) -> FileTags:
        raise NotImplementedError

    @abstractmethod
    def update(self, song: Song, artwork: Artwork | None = None) -> FileTags:
        raise NotImplementedError
