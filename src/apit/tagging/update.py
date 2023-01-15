from pathlib import Path

from .mp4 import to_file_tags
from .mp4 import update_metadata
from apit.file_tags import FileTags
from apit.metadata import Song


def update_tags(file: Path, song: Song, cover_path: Path | None = None) -> FileTags:
    return to_file_tags(update_metadata(file, song, cover_path))
