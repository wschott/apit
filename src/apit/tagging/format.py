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
    def get_by(cls, file: Path) -> type[Format]:
        extension = file.suffix[1:]
        for format in cls.registry:
            if extension in format.extensions:
                return format
        raise ApitUnsupportedFileTypeError(extension)

    @classmethod
    def get_supported_extensions(cls) -> list[str]:
        return flatten([format.extensions for format in cls.registry])

    @staticmethod
    @abstractmethod
    def read(file: Path) -> FileTags:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def update(file: Path, song: Song, artwork: Artwork | None = None) -> FileTags:
        raise NotImplementedError
