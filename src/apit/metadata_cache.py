import logging
import os
import re
from pathlib import Path
from typing import List

from apit.metadata import Album


def _generate_cache_filename(album: Album) -> str:
    filename_parts = [
        album['artistName'],
        album['collectionName'],
        album['collectionId']
    ]
    filename: List[str] = [re.sub(r'\W+', '_', str(f)) for f in filename_parts]
    return f'{"-".join(filename)}.json'

def save_to_cache(json: str, cache_path: Path, album: Album) -> None:
    cache_file = cache_path / _generate_cache_filename(album)

    if not cache_path.exists():
        os.makedirs(cache_path)

    cache_file.write_text(json)
    logging.info('Downloaded metadata cached in: %s', cache_file)
