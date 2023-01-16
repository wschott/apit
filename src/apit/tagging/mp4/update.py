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

ARTWORK_FORMATS = {
    ".jpg": mutagen.mp4.MP4Cover.FORMAT_JPEG,
    ".png": mutagen.mp4.MP4Cover.FORMAT_PNG,
}


def update_metadata(
    file: Path, song: Song, cover_path: Path | None = None
) -> mutagen.mp4.MP4:
    mp4_file = read_metadata_raw(file)

    if mp4_file.tags is None:
        mp4_file.add_tags()

    if is_itunes_bought_file(mp4_file):
        raise ApitError("original iTunes Store file")

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
    try:
        image_format = ARTWORK_FORMATS[artwork_path.suffix]
    except KeyError:
        raise ApitError(f"Unknown artwork image type: {artwork_path.suffix}")
    else:
        return mutagen.mp4.MP4Cover(artwork_path.read_bytes(), imageformat=image_format)


def _modify_mp4_file(
    mp4_file: mutagen.mp4.MP4, song: Song, artwork: mutagen.mp4.MP4Cover | None = None
) -> mutagen.mp4.MP4:
    mp4_file[MP4_MAPPING.ARTIST.value] = song.artist
    mp4_file[MP4_MAPPING.TITLE.value] = song.title
    mp4_file[MP4_MAPPING.ALBUM_NAME.value] = song.album_name
    mp4_file[MP4_MAPPING.GENRE.value] = song.genre
    mp4_file[MP4_MAPPING.RELEASE_DATE.value] = song.release_date
    mp4_file[MP4_MAPPING.DISC_NUMBER.value] = [(song.disc_number, song.disc_total)]
    mp4_file[MP4_MAPPING.TRACK_NUMBER.value] = [(song.track_number, song.track_total)]
    mp4_file[MP4_MAPPING.RATING.value] = [RATING_MAPPING[to_rating(song.rating)]]
    mp4_file[MP4_MAPPING.MEDIA_TYPE.value] = [
        ITEM_KIND_MAPPING[to_item_kind(song.media_kind)]
    ]
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


BLACKLIST: list[str] = [
    MP4_MAPPING.OWNER_NAME,
    MP4_MAPPING.USER_MAIL,
]


def is_itunes_bought_file(mp4_file: mutagen.mp4.MP4) -> bool:
    if not mp4_file.tags:
        return False

    return any(item in mp4_file.tags for item in BLACKLIST)
