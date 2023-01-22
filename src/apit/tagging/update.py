from pathlib import Path

from .format import Format
from apit.file_tags import FileTags
from apit.metadata import Artwork
from apit.metadata import Song


def update_tags(file: Path, song: Song, artwork: Artwork | None = None) -> FileTags:
    return Format.get_by(file).update(file, song, artwork)
