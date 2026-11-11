from pathlib import Path
from typing import override

from .read import read_metadata_raw
from .to_file_tags import to_file_tags
from .update import update_metadata
from apit.core.audio.audio_file import AudioFile
from apit.core.audio.file_tags import FileTags
from apit.core.metadata.artwork import Artwork
from apit.core.metadata.song import Song


class Mp3File(AudioFile):
    def __init__(self, file: Path) -> None:
        self.file: Path = file

    @override
    def read(self) -> FileTags:
        return to_file_tags(read_metadata_raw(self.file))

    @override
    def update(self, song: Song, artwork: Artwork | None = None) -> FileTags:
        return to_file_tags(update_metadata(self.file, song, artwork))
