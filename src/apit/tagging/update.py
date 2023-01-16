from pathlib import Path

from . import format_registry
from apit.file_tags import FileTags
from apit.metadata import Song


def update_tags(file: Path, song: Song, cover_path: Path | None = None) -> FileTags:
    return format_registry.get_by(file).update(file, song, cover_path)
