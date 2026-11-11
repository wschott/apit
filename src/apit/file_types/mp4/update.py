from pathlib import Path
from typing import Final

import mutagen.mp4

from .constants import Mp4Mapping
from .fields import MP4_FIELDS
from .read import read_metadata_raw
from apit.core.errors import ApitError
from apit.core.metadata.artwork import Artwork
from apit.core.metadata.song import Song


def update_metadata(
    file: Path, song: Song, artwork: Artwork | None = None
) -> mutagen.mp4.MP4:
    mp4_file = read_metadata_raw(file)

    if mp4_file.tags is None:
        mp4_file.add_tags()

    if is_itunes_bought_file(mp4_file):
        raise ApitError("original iTunes Store file")

    _modify_mp4_file(mp4_file, song, artwork)
    # TODO error handling
    try:
        mp4_file.save()
    except Exception as e:
        raise ApitError(e)
    else:
        return mp4_file


def _modify_mp4_file(
    mp4_file: mutagen.mp4.MP4, song: Song, artwork: Artwork | None = None
) -> mutagen.mp4.MP4:
    for field in MP4_FIELDS:
        if field.encode is None:
            continue
        if (atom := field.encode(field.tag_id, song, artwork)) is not None:
            mp4_file[field.tag_id.value] = atom

    # command.append(f'--xID "{track[]}"')
    # if track.genre in GENRE_MAP:
    #     command.append(f'--geID "{GENRE_MAP[track.genre]}"')
    # native tag writing for the following isn't supported by AtomicParsley yet
    # command.append(f'--atID "{track.artist_id}"')
    # command.append(f'--plID "{track.collection_Id}"')

    return mp4_file


BLACKLIST: Final[list[str]] = [
    Mp4Mapping.OWNER_NAME,
    Mp4Mapping.USER_MAIL,
]


def is_itunes_bought_file(mp4_file: mutagen.mp4.MP4) -> bool:
    if not mp4_file.tags:
        return False

    return any(item in mp4_file.tags for item in BLACKLIST)
