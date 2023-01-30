from pathlib import Path

from .read import read_metadata_raw
from .to_file_tags import to_file_tags
from .update import update_metadata
from apit.file_tags import FileTags
from apit.file_type.audio_file import AudioFile
from apit.file_type.audio_file import AudioFileFactory
from apit.metadata import Artwork
from apit.metadata import Song


@AudioFileFactory.register("m4a")
class Mp4File(AudioFile):
    def __init__(self, file: Path) -> None:
        self.file: Path = file

    def read(self) -> FileTags:
        return to_file_tags(read_metadata_raw(self.file))

    def update(self, song: Song, artwork: Artwork | None = None) -> FileTags:
        return to_file_tags(update_metadata(self.file, song, artwork))