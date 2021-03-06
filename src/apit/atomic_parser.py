from pathlib import Path
from typing import Optional

import mutagen
import mutagen.mp4

from apit.error import ApitError
from apit.metadata import Song
from apit.store.constants import (
    BLACKLIST,
    ITEM_KIND_MAPPING,
    MP4_MAPPING,
    RATING_MAPPING,
    to_item_kind,
    to_rating,
)


def read_metadata(file: Path) -> mutagen.mp4.MP4:
    try:
        return mutagen.mp4.MP4(file)
    except mutagen.MutagenError as e:
        raise ApitError(e)


def is_itunes_bought_file(file: Path) -> bool:
    try:
        mp4_file = read_metadata(file)
        if not mp4_file.tags:
            raise ApitError("No tags present")
    except ApitError:
        return False
    else:
        return any(map(lambda item: item in mp4_file.tags, BLACKLIST))


def update_metadata(file: Path, song: Song, cover_path: Optional[Path] = None) -> mutagen.mp4.MP4:
    mp4_file = read_metadata(file)

    if cover_path:
        artwork = _read_artwork_content(cover_path)
        _modify_mp4_file(mp4_file, song, artwork)
    else:
        _modify_mp4_file(mp4_file, song)
    # TODO error handling
    try:
        mp4_file.save()
    except Exception as e:
        raise ApitError(e)
    else:
        return mp4_file


def _read_artwork_content(artwork_path: Path) -> mutagen.mp4.MP4Cover:
    artwork_content = artwork_path.read_bytes()
    if artwork_path.suffix == '.jpg':
        return mutagen.mp4.MP4Cover(artwork_content, imageformat=mutagen.mp4.MP4Cover.FORMAT_JPEG)
    elif artwork_path.suffix == '.png':
        return mutagen.mp4.MP4Cover(artwork_content, imageformat=mutagen.mp4.MP4Cover.FORMAT_PNG)
    raise ApitError('Unknown artwork image type')


def _modify_mp4_file(mp4_file: mutagen.mp4.MP4, song: Song, artwork: mutagen.mp4.MP4Cover = None) -> mutagen.mp4.MP4:
    mp4_file[MP4_MAPPING.ARTIST.value] = song.artist
    mp4_file[MP4_MAPPING.TITLE.value] = song.title
    mp4_file[MP4_MAPPING.ALBUM_NAME.value] = song.album_name
    mp4_file[MP4_MAPPING.GENRE.value] = song.genre
    mp4_file[MP4_MAPPING.RELEASE_DATE.value] = song.release_date
    mp4_file[MP4_MAPPING.DISC_NUMBER.value] = [(song.disc_number, song.disc_total)]
    mp4_file[MP4_MAPPING.TRACK_NUMBER.value] = [(song.track_number, song.track_total)]
    mp4_file[MP4_MAPPING.RATING.value] = [RATING_MAPPING[to_rating(song.rating)]]
    mp4_file[MP4_MAPPING.MEDIA_TYPE.value] = [ITEM_KIND_MAPPING[to_item_kind(song.media_kind)]]
    mp4_file[MP4_MAPPING.ALBUM_ARTIST.value] = song.album_artist
    mp4_file[MP4_MAPPING.COPYRIGHT.value] = song.copyright
    mp4_file[MP4_MAPPING.COMPILATION.value] = song.compilation
    mp4_file[MP4_MAPPING.CONTENT_ID.value] = [song.content_id]

    if artwork:
        # TODO first, remove all artwork
        mp4_file[MP4_MAPPING.ARTWORK.value] = [artwork]

    # command.append(f'--xID "{track[]}"')
    # if track.genre in GENRE_MAP:
    #     command.append(f'--geID "{GENRE_MAP[track.genre]}"')
    # native tag writing for the following isn't supported by AtomicParsley yet
    # command.append(f'--atID "{track.artist_id}"')
    # command.append(f'--plID "{track.collection_Id}"')

    return mp4_file
