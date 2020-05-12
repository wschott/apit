from pathlib import Path
from subprocess import CompletedProcess
from typing import List

from apit.cmd import execute_command
from apit.metadata import Album, Song

BLACKLIST = [
    'Atom "ownr" contains',
    'Atom "apID" contains',
]

RATING_MAP = {
    'cleaned': 'clean',
    'explicit': 'explicit',
    'notExplicit': 'remove',
}

ITEM_TYPE_MAP = {
    'song': 'Normal',
}


# https://affiliate.itunes.apple.com/resources/documentation/genre-mapping/
# GENRE_MAP = {
#     'Hip Hop/Rap': 18,
#     'Hip-Hop/Rap': 18,
#     'Dance': 17,
#     'Rock': 21,
# }

def read_metadata(file: Path) -> CompletedProcess:
    command = ['-t']
    return execute_command(file, command)


def is_itunes_bought_file(file: Path) -> bool:
    command_status = read_metadata(file)
    return any(map(lambda item: item in command_status.stdout, BLACKLIST))


def update_metadata(file: Path, album: Album, song: Song, should_overwrite: bool) -> CompletedProcess:
    command = _generate_metadata_update_command(album, song, should_overwrite)
    return execute_command(file, command, shell=True)


def _generate_metadata_update_command(album_metadata: Album, track_metadata: Song, should_overwrite: bool) -> List[str]:
    command = [
        f'--artist "{track_metadata["artistName"]}"',
        f'--title "{track_metadata["trackCensoredName"]}"',
        f'--album "{track_metadata["collectionName"]}"',
        f'--genre "{track_metadata["primaryGenreName"]}"',
        f'--year "{track_metadata["releaseDate"]}"',
        f'--disknum {track_metadata["discNumber"]}/{track_metadata["discCount"]}',
        f'--tracknum {track_metadata["trackNumber"]}/{track_metadata["trackCount"]}',
        f'--advisory {RATING_MAP[track_metadata["trackExplicitness"]]}',
        f'--stik "{ITEM_TYPE_MAP[track_metadata["kind"]]}"',
        f'--albumArtist "{album_metadata["artistName"]}"',
        f'--copyright "{album_metadata["copyright"]}"',
        f'--cnID "{track_metadata["trackId"]}"',
    ]

    # command.append(f'--xID "{track[]}"')

    # if track['primaryGenreName'] in GENRE_MAP:
    #     command.append(f'--geID "{GENRE_MAP[track["primaryGenreName"]]}"')

    # native tag writing for the following isn't supported by AtomicParsley yet
    # command.append(f'--atID "{track["artistId"]}"')
    # command.append(f'--plID "{track["collectionId"]}"')

    if should_overwrite:
        command.append('--overWrite')

    return command
