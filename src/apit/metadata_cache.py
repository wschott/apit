import os
import re
from pathlib import Path
from typing import List

from apit.metadata import Song


def generate_cache_filename(cache_path: Path, song: Song) -> Path:
    filename_parts = [
        song.album_artist,
        song.album_name,
        song.collection_id,
    ]
    filename: List[str] = [re.sub(r'\W+', '_', str(f)) for f in filename_parts]
    return cache_path / f'{"-".join(filename)}.json'


def save_to_cache(json: str, cache_file: Path) -> None:
    if not cache_file.parent.exists():
        os.makedirs(cache_file.parent)
    cache_file.write_text(json)
