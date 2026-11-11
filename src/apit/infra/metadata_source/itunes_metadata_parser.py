import json
from collections.abc import Iterable
from collections.abc import Mapping
from typing import Any
from typing import Final
from typing import override

from .constants import StoreKind
from .constants import StoreRating
from .constants import StoreKey
from apit.core.metadata.album import Album
from apit.core.metadata.media_kind import MediaKind
from apit.core.metadata.rating import Rating
from apit.core.metadata.disc_number import DiscNumber
from apit.core.metadata.track_number import TrackNumber
from apit.core.metadata.song import Song
from apit.core.metadata_parser import ApitMetadataParsingError
from apit.core.metadata_parser import MetadataParser


class ItunesMetadataParser(MetadataParser):
    @override
    def extract_songs(self, metadata_json: str) -> list[Song]:
        try:
            itunes_data = json.loads(metadata_json)
        except json.JSONDecodeError:
            raise ApitMetadataParsingError(
                "Apple Music/iTunes Store metadata results format error"
            )

        if "results" not in itunes_data or not itunes_data["results"]:
            raise ApitMetadataParsingError(
                "Apple Music/iTunes Store metadata results empty"
            )

        return _find_songs(itunes_data["results"], _find_album(itunes_data["results"]))


def _find_album(music_data: Iterable[Mapping[str, Any]]) -> Album:
    for item in music_data:
        if (
            StoreKey.COLLECTION_TYPE.value in item
            and item[StoreKey.COLLECTION_TYPE.value] == StoreKind.ALBUM_COLLECTION.value
        ):
            return to_album(item)
    raise ApitMetadataParsingError("No album found in metadata")


def _find_songs(music_data: Iterable[Mapping[str, Any]], album: Album) -> list[Song]:
    return [
        to_song(album, item)
        for item in music_data
        if StoreKey.MEDIA_KIND.value in item
        and item[StoreKey.MEDIA_KIND.value] == StoreKind.SONG.value
    ]


def to_album(item: Mapping[str, Any]) -> Album:
    return Album(
        album_artist=_extract_by_key(StoreKey.ALBUM_ARTIST, item),
        copyright=_extract_by_key(StoreKey.COPYRIGHT, item),
        artwork_url=_extract_by_key(StoreKey.ARTWORK_URL, item),
    )


def to_song(album: Album, item: Mapping[str, Any]) -> Song:
    try:
        _ = _extract_by_key(StoreKey.COLLECTION_ARTIST, item)
    except ApitMetadataParsingError:
        is_compilation = False
    else:
        is_compilation = True

    return Song(
        album=album,
        track_number=TrackNumber(_extract_by_key(StoreKey.TRACK_NUMBER, item)),
        track_total=_extract_by_key(StoreKey.TRACK_TOTAL, item),
        disc_number=DiscNumber(_extract_by_key(StoreKey.DISC_NUMBER, item)),
        disc_total=_extract_by_key(StoreKey.DISC_TOTAL, item),
        title=_extract_by_key(StoreKey.TITLE, item),
        artist=_extract_by_key(StoreKey.ARTIST, item),
        release_date=_extract_by_key(StoreKey.RELEASE_DATE, item),
        genre=_extract_by_key(StoreKey.GENRE, item),
        album_name=_extract_by_key(StoreKey.ALBUM_NAME, item),
        content_id=_extract_by_key(StoreKey.CONTENT_ID, item),
        collection_id=_extract_by_key(StoreKey.COLLECTION_ID, item),
        rating=to_rating(
            StoreRating.from_rating_str(_extract_by_key(StoreKey.RATING, item))
        ),
        media_kind=to_media_kind(
            StoreKind.from_kind_str(_extract_by_key(StoreKey.MEDIA_KIND, item))
        ),
        compilation=is_compilation,
    )


STORE_RATING_TO_RATING_MAPPING: Final[dict[StoreRating, Rating]] = {
    StoreRating.NONE: Rating.NONE,
    StoreRating.EXPLICIT: Rating.EXPLICIT,
    StoreRating.CLEAN: Rating.CLEAN,
}


def to_rating(store_rating: StoreRating) -> Rating:
    rating = STORE_RATING_TO_RATING_MAPPING.get(store_rating)
    if rating is None:
        raise ApitMetadataParsingError(f"Unknown rating: {store_rating}")
    else:
        return rating


STORE_KIND_TO_MEDIA_KIND_MAPPING: Final[dict[StoreKind, MediaKind]] = {
    StoreKind.ALBUM: MediaKind.ALBUM,
    StoreKind.SONG: MediaKind.SONG,
}


def to_media_kind(store_kind: StoreKind) -> MediaKind:
    media_kind = STORE_KIND_TO_MEDIA_KIND_MAPPING.get(store_kind)
    if media_kind is None:
        raise ApitMetadataParsingError(f"Unknown kind: {media_kind}")
    else:
        return media_kind


def _extract_by_key(key: StoreKey, item: Mapping[str, Any]) -> Any:
    if not isinstance(key, StoreKey):
        raise ApitMetadataParsingError(f"Unknown metadata key: {key}")
    if key not in item:
        raise ApitMetadataParsingError(f"Metadata key not found in metadata: {key}")
    return item[key]
