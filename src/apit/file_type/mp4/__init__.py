from .read import read_metadata_raw
from .to_file_tags import to_file_tags
from .update import update_metadata
from apit.file_tags import FileTags
from apit.file_type.audio_file import AudioFile
from apit.metadata import Artwork
from apit.metadata import Song


class Mp4File(AudioFile):
    extensions = ["m4a"]

    def read(self) -> FileTags:
        return to_file_tags(read_metadata_raw(self.file))

    def update(self, song: Song, artwork: Artwork | None = None) -> FileTags:
        return to_file_tags(update_metadata(self.file, song, artwork))
