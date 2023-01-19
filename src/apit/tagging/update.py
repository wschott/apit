from pathlib import Path

from . import format_registry
from apit.file_tags import FileTags
from apit.metadata import Artwork
from apit.metadata import Song


def update_tags(file: Path, song: Song, artwork: Artwork | None = None) -> FileTags:
    return format_registry.get_by(file).update(file, song, artwork)
