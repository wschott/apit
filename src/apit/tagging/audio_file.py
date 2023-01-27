from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path

from apit.error import ApitUnsupportedAudioFileError
from apit.file_tags import FileTags
from apit.list_utils import flatten
from apit.metadata import Artwork
from apit.metadata import Song
from apit.registry_mixin import RegistryMixin


class AudioFile(ABC, RegistryMixin):
    extensions: list[str] = []

    @classmethod
    def from_(cls, file: Path) -> AudioFile:
        extension = file.suffix[1:]
        for file_format in cls.registry:
            if extension in file_format.extensions:
                return file_format(file)
        raise ApitUnsupportedAudioFileError(extension)

    @classmethod
    def get_supported_extensions(cls) -> list[str]:
        return flatten([file_format.extensions for file_format in cls.registry])

    def __init__(self, file: Path) -> None:
        self.file: Path = file

    @abstractmethod
    def read(self) -> FileTags:
        raise NotImplementedError

    @abstractmethod
    def update(self, song: Song, artwork: Artwork | None = None) -> FileTags:
        raise NotImplementedError
