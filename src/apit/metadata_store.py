import os
import re
from pathlib import Path
from typing import List

from apit.album import Album
from apit.musicdata import extract_album_and_song_data


def _generate_log_filename(album: Album) -> str:
    filename_parts = [
        album['artistName'],
        album['collectionName'],
        album['collectionId']
    ]
    filename: List[str] = [re.sub(r'\W+', '_', str(f)) for f in filename_parts]
    return f'{"-".join(filename)}.json'

def save_log(json: str, log_path: Path):
    album = extract_album_and_song_data(json)
    log_file = log_path / _generate_log_filename(album)

    if not log_path.exists():
        os.makedirs(log_path)

    log_file.write_text(json)
    return log_file
