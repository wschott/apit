from pathlib import Path
from typing import cast

import mutagen.id3
import mutagen.mp3

from .fields import MP3_FIELDS
from .read import read_metadata_raw
from apit.core.errors import ApitError
from apit.core.metadata.artwork import Artwork
from apit.core.metadata.song import Song


def update_metadata(
    file: Path, song: Song, artwork: Artwork | None = None
) -> mutagen.mp3.MP3:
    mp3_file = read_metadata_raw(file)

    if mp3_file.tags is None:
        mp3_file.add_tags()

    _modify_mp3_file(mp3_file, song, artwork)
    # TODO error handling
    try:
        mp3_file.save()
    except Exception as e:
        raise ApitError(e)
    else:
        return mp3_file


def _modify_mp3_file(
    mp3_file: mutagen.mp3.MP3, song: Song, artwork: Artwork | None = None
) -> mutagen.mp3.MP3:
    tags = cast(mutagen.id3.ID3, mp3_file.tags)
    for field in MP3_FIELDS:
        if field.encode is None:
            continue
        if (frames := field.encode(field.tag_id, song, artwork)) is not None:
            tags.setall(field.tag_id.value, frames)

    return mp3_file
