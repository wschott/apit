from .read import read_metadata_raw
from .to_file_tags import to_file_tags
from .update import update_metadata
from apit.file_tags import FileTags
from apit.metadata import Artwork
from apit.metadata import Song
from apit.tagging.audio_file import AudioFile


class Mp3File(AudioFile):
    extensions = ["mp3"]

    def read(self) -> FileTags:
        return to_file_tags(read_metadata_raw(self.file))

    def update(self, song: Song, artwork: Artwork | None = None) -> FileTags:
        return to_file_tags(update_metadata(self.file, song, artwork))
