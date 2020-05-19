import logging
from pathlib import Path
from subprocess import CompletedProcess
from typing import List, Optional

from apit.cmd import execute_command
from apit.error import ApitError
from apit.metadata import Song
from apit.store.constants import (
    AP_ITEM_KIND_MAPPING,
    AP_RATING_MAPPING,
    BLACKLIST,
    to_item_kind,
    to_rating,
)


def read_metadata(file: Path) -> CompletedProcess:
    command = ['-t']
    command_status = execute_command(file, command)

    logging.info('Command: %s', command_status.args)
    if bool(command_status.returncode):
        raise ApitError({'stdout': command_status.stdout.strip(), 'stderr': command_status.stderr.strip()})
    return command_status.stdout.strip()


def is_itunes_bought_file(file: Path) -> bool:
    try:
        result = read_metadata(file)
    except ApitError:
        return False
    else:
        return any(map(lambda item: item in result, BLACKLIST))


def update_metadata(file: Path, song: Song, should_overwrite: bool, cover_path: Optional[Path] = None):
    command = _generate_metadata_update_command(song, should_overwrite, cover_path)
    command_status = execute_command(file, command, shell=True)

    logging.info('Command: %s', command_status.args)
    if bool(command_status.returncode):
        raise ApitError({'stdout': command_status.stdout.strip(), 'stderr': command_status.stderr.strip()})
    return command_status.stdout.strip()


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
