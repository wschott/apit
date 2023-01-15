from pathlib import Path

import mutagen.mp4

from .constants import MP4_MAPPING
from .read import read_metadata_raw
from apit.error import ApitError
from apit.metadata import Song
from apit.store.constants import ITEM_KIND_MAPPING
from apit.store.constants import RATING_MAPPING
from apit.store.constants import to_item_kind
from apit.store.constants import to_rating


def update_metadata(
    file: Path, song: Song, cover_path: Path | None = None
) -> mutagen.mp4.MP4:
    mp4_file = read_metadata_raw(file)

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
    if artwork_path.suffix == ".jpg":
        return mutagen.mp4.MP4Cover(
            artwork_content, imageformat=mutagen.mp4.MP4Cover.FORMAT_JPEG
        )
    elif artwork_path.suffix == ".png":
        return mutagen.mp4.MP4Cover(
            artwork_content, imageformat=mutagen.mp4.MP4Cover.FORMAT_PNG
        )
    raise ApitError("Unknown artwork image type")


def _modify_mp4_file(
    mp4_file: mutagen.mp4.MP4, song: Song, artwork: mutagen.mp4.MP4Cover | None = None
) -> mutagen.mp4.MP4:
    mp4_file[MP4_MAPPING.ARTIST] = song.artist
    mp4_file[MP4_MAPPING.TITLE] = song.title
    mp4_file[MP4_MAPPING.ALBUM_NAME] = song.album_name
    mp4_file[MP4_MAPPING.GENRE] = song.genre
    mp4_file[MP4_MAPPING.RELEASE_DATE] = song.release_date
    mp4_file[MP4_MAPPING.DISC_NUMBER] = [(song.disc_number, song.disc_total)]
    mp4_file[MP4_MAPPING.TRACK_NUMBER] = [(song.track_number, song.track_total)]
    mp4_file[MP4_MAPPING.RATING] = [RATING_MAPPING[to_rating(song.rating)]]
    mp4_file[MP4_MAPPING.MEDIA_TYPE] = [
        ITEM_KIND_MAPPING[to_item_kind(song.media_kind)]
    ]
    mp4_file[MP4_MAPPING.ALBUM_ARTIST] = song.album_artist
    mp4_file[MP4_MAPPING.COPYRIGHT] = song.copyright
    mp4_file[MP4_MAPPING.COMPILATION] = song.compilation
    mp4_file[MP4_MAPPING.CONTENT_ID] = [song.content_id]

    if artwork:
        # TODO first, remove all artwork
        mp4_file[MP4_MAPPING.ARTWORK] = [artwork]

    # command.append(f'--xID "{track[]}"')
    # if track.genre in GENRE_MAP:
    #     command.append(f'--geID "{GENRE_MAP[track.genre]}"')
    # native tag writing for the following isn't supported by AtomicParsley yet
    # command.append(f'--atID "{track.artist_id}"')
    # command.append(f'--plID "{track.collection_Id}"')

    return mp4_file
