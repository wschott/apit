from pathlib import Path
from subprocess import CompletedProcess
from typing import List, Optional

from apit.cmd import execute_command
from apit.metadata import Song
from apit.store.constants import (
    AP_ITEM_KIND_MAPPING,
    AP_RATING_MAPPING,
    to_item_kind,
    to_rating,
)

BLACKLIST = [
    'Atom "ownr" contains',
    'Atom "apID" contains',
]


def read_metadata(file: Path) -> CompletedProcess:
    command = ['-t']
    return execute_command(file, command)


def is_itunes_bought_file(file: Path) -> bool:
    command_status = read_metadata(file)
    return any(map(lambda item: item in command_status.stdout, BLACKLIST))


def update_metadata(file: Path, song: Song, should_overwrite: bool, cover_path: Optional[Path] = None) -> CompletedProcess:
    command = _generate_metadata_update_command(song, should_overwrite, cover_path)
    return execute_command(file, command, shell=True)


def _generate_metadata_update_command(track: Song, should_overwrite: bool, cover_path: Optional[Path] = None) -> List[str]:
    command = [
        f'--artist "{track.artist}"',
        f'--title "{track.title}"',
        f'--album "{track.album_name}"',
        f'--genre "{track.genre}"',
        f'--year "{track.release_date}"',
        f'--disknum {track.disc_number}/{track.disc_total}',
        f'--tracknum {track.track_number}/{track.track_total}',
        f'--advisory {AP_RATING_MAPPING[to_rating(track.rating)]}',
        f'--stik "{AP_ITEM_KIND_MAPPING[to_item_kind(track.media_kind)]}"',
        f'--albumArtist "{track.album_artist}"',
        f'--copyright "{track.copyright}"',
        f'--compilation {to_atomicparsley_bool(track.compilation)}',
        f'--cnID "{track.content_id}"',
    ]
    if cover_path:
        command.append(f'--artwork REMOVE_ALL --artwork {cover_path}')  # first, remove all artwork

    # command.append(f'--xID "{track[]}"')

    # if track.genre in GENRE_MAP:
    #     command.append(f'--geID "{GENRE_MAP[track.genre]}"')

    # native tag writing for the following isn't supported by AtomicParsley yet
    # command.append(f'--atID "{track.artist_id}"')
    # command.append(f'--plID "{track.collection_Id}"')

    if should_overwrite:
        command.append('--overWrite')

    return command


def to_atomicparsley_bool(value) -> str:
    return "true" if value else "false"
