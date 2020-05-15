import json
from typing import Any, Dict, List

from apit.error import ApitError
from apit.metadata import Album, Song
from apit.store.constants import (
    COLLECTION_TYPE_KEY,
    KIND_KEY,
    STORE_KEY,
    VALID_COLLECTION_TYPE_FOR_ALBUM,
    VALID_KIND_VALUES_FOR_SONG,
)


def extract_songs(metadata_json: str) -> List[Song]:
    try:
        itunes_data = json.loads(metadata_json)
    except json.JSONDecodeError:
        raise ApitError('Apple Music/iTunes Store metadata results format error')

    if 'results' not in itunes_data or 'resultCount' not in itunes_data or itunes_data['resultCount'] == 0:
        raise ApitError('Apple Music/iTunes Store metadata results empty')

    return _find_songs(itunes_data['results'], _find_album(itunes_data['results']))


def _find_album(music_data: List[Dict[str, Any]]) -> Album:
    for item in music_data:
        if COLLECTION_TYPE_KEY in item and item[COLLECTION_TYPE_KEY] == VALID_COLLECTION_TYPE_FOR_ALBUM:
            return to_album(item)
    raise ApitError('No album found in metadata')


def _find_songs(music_data: List[Dict[str, Any]], album: Album) -> List[Song]:
    return [to_song(album, item) for item in music_data if KIND_KEY in item and item[KIND_KEY] == VALID_KIND_VALUES_FOR_SONG]


def to_album(item: Dict[str, Any]) -> Album:
    return Album(
        album_artist=extract_by_key(STORE_KEY.ALBUM_ARTIST, item),
        copyright=extract_by_key(STORE_KEY.COPYRIGHT, item),
    )


def to_song(album: Album, item: Dict[str, Any]) -> Song:
    try:
        _ = extract_by_key(STORE_KEY.COLLECTION_ARTIST, item)
    except ApitError:
        is_compilation = False
    else:
        is_compilation = True

    return Song(
        album=album,
        track_number=extract_by_key(STORE_KEY.TRACK_NUMBER, item),
        track_total=extract_by_key(STORE_KEY.TRACK_TOTAL, item),
        disc_number=extract_by_key(STORE_KEY.DISC_NUMBER, item),
        disc_total=extract_by_key(STORE_KEY.DISC_TOTAL, item),
        title=extract_by_key(STORE_KEY.TITLE, item),
        artist=extract_by_key(STORE_KEY.ARTIST, item),
        release_date=extract_by_key(STORE_KEY.RELEASE_DATE, item),
        genre=extract_by_key(STORE_KEY.GENRE, item),
        album_name=extract_by_key(STORE_KEY.ALBUM_NAME, item),
        content_id=extract_by_key(STORE_KEY.CONTENT_ID, item),
        collection_id=extract_by_key(STORE_KEY.COLLECTION_ID, item),
        # TODO convert to enum?
        rating=extract_by_key(STORE_KEY.RATING, item),
        # TODO convert to enum?
        media_kind=extract_by_key(STORE_KEY.MEDIA_KIND, item),
        compilation=is_compilation,
    )


def extract_by_key(key: STORE_KEY, item: Dict[str, Any]) -> Any:
    if not isinstance(key, STORE_KEY):
        raise ApitError('Unknown metadata key: %s' % key)
    if key.value not in item:
        raise ApitError('Metadata key not found in metadata: %s' % key.value)
    return item[key.value]
