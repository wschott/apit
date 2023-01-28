import json
from typing import Any

from .constants import COLLECTION_TYPE_KEY
from .constants import KIND_KEY
from .constants import StoreKey
from .constants import VALID_COLLECTION_TYPE_FOR_ALBUM
from .constants import VALID_KIND_VALUES_FOR_SONG
from apit.error import ApitError
from apit.metadata import Album
from apit.metadata import Song
from apit.types import DiscNumber
from apit.types import TrackNumber


def extract_songs(metadata_json: str) -> list[Song]:
    try:
        itunes_data = json.loads(metadata_json)
    except json.JSONDecodeError:
        raise ApitError("Apple Music/iTunes Store metadata results format error")

    if "results" not in itunes_data or not itunes_data["results"]:
        raise ApitError("Apple Music/iTunes Store metadata results empty")

    return _find_songs(itunes_data["results"], _find_album(itunes_data["results"]))


def _find_album(music_data: list[dict[str, Any]]) -> Album:
    for item in music_data:
        if (
            COLLECTION_TYPE_KEY in item
            and item[COLLECTION_TYPE_KEY] == VALID_COLLECTION_TYPE_FOR_ALBUM
        ):
            return to_album(item)
    raise ApitError("No album found in metadata")


def _find_songs(music_data: list[dict[str, Any]], album: Album) -> list[Song]:
    return [
        to_song(album, item)
        for item in music_data
        if KIND_KEY in item and item[KIND_KEY] == VALID_KIND_VALUES_FOR_SONG
    ]


def to_album(item: dict[str, Any]) -> Album:
    return Album(
        album_artist=extract_by_key(StoreKey.ALBUM_ARTIST, item),
        copyright=extract_by_key(StoreKey.COPYRIGHT, item),
        artwork_url=extract_by_key(StoreKey.ARTWORK_URL, item),
    )


def to_song(album: Album, item: dict[str, Any]) -> Song:
    try:
        _ = extract_by_key(StoreKey.COLLECTION_ARTIST, item)
    except ApitError:
        is_compilation = False
    else:
        is_compilation = True

    return Song(
        album=album,
        track_number=TrackNumber(extract_by_key(StoreKey.TRACK_NUMBER, item)),
        track_total=extract_by_key(StoreKey.TRACK_TOTAL, item),
        disc_number=DiscNumber(extract_by_key(StoreKey.DISC_NUMBER, item)),
        disc_total=extract_by_key(StoreKey.DISC_TOTAL, item),
        title=extract_by_key(StoreKey.TITLE, item),
        artist=extract_by_key(StoreKey.ARTIST, item),
        release_date=extract_by_key(StoreKey.RELEASE_DATE, item),
        genre=extract_by_key(StoreKey.GENRE, item),
        album_name=extract_by_key(StoreKey.ALBUM_NAME, item),
        content_id=extract_by_key(StoreKey.CONTENT_ID, item),
        collection_id=extract_by_key(StoreKey.COLLECTION_ID, item),
        # TODO convert to enum?
        rating=extract_by_key(StoreKey.RATING, item),
        # TODO convert to enum?
        media_kind=extract_by_key(StoreKey.MEDIA_KIND, item),
        compilation=is_compilation,
    )


def extract_by_key(key: StoreKey, item: dict[str, Any]) -> Any:
    if not isinstance(key, StoreKey):
        raise ApitError(f"Unknown metadata key: {key}")
    if key not in item:
        raise ApitError("Metadata key not found in metadata: %s" % key)
    return item[key]
