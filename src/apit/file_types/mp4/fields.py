from collections.abc import Mapping
from typing import Any
from typing import Final

import mutagen.mp4

from .constants import ITEM_KIND_FROM_MAPPING
from .constants import ITEM_KIND_MAPPING
from .constants import Mp4Mapping
from .constants import RATING_FROM_MAPPING
from .constants import RATING_MAPPING
from apit.core.audio.tag_id import TagIdEnum
from apit.core.audio.tag_name import TagName
from apit.core.audio.tag_value import ArtworkValue
from apit.core.audio.tag_value import FlagValue
from apit.core.audio.tag_value import LyricsValue
from apit.core.audio.tag_value import MediaKindValue
from apit.core.audio.tag_value import NumberOfTotalValue
from apit.core.audio.tag_value import RatingValue
from apit.core.audio.tag_value import TagValue
from apit.core.audio.tag_value import TextValue
from apit.core.errors import ApitError
from apit.core.metadata.artwork import Artwork
from apit.core.metadata.song import Song
from apit.file_types.field import Field
from apit.utils.mime_type import MimeType

MP4_COVER_FORMAT_MAPPING: Final[Mapping[MimeType, int]] = {
    MimeType.JPEG: mutagen.mp4.MP4Cover.FORMAT_JPEG,
    MimeType.PNG: mutagen.mp4.MP4Cover.FORMAT_PNG,
}


def decode_default(raw: Any) -> TagValue:
    if isinstance(raw, list):  # most mp4 tags
        return TextValue("".join(str(x) for x in raw))
    return TextValue(str(raw))


def _decode_flag(raw: Any) -> TagValue:
    value = raw  # no list
    return FlagValue(bool(value))


def _decode_rating(raw: Any) -> TagValue:
    value = raw[0]  # list
    if (rating := RATING_FROM_MAPPING.get(int(value))) is not None:
        return RatingValue(rating)
    return decode_default(raw)


def _decode_media_kind(raw: Any) -> TagValue:
    value = raw[0]  # list
    if (kind := ITEM_KIND_FROM_MAPPING.get(value)) is not None:
        return MediaKindValue(kind)
    return decode_default(raw)


def _decode_lyrics(raw: Any) -> TagValue:
    value = raw[0]  # list
    return LyricsValue(value)


def _decode_artwork(raw: Any) -> TagValue:
    value = len(raw)  # list
    return ArtworkValue(value)


def _decode_number_of_total(raw: Any) -> TagValue:
    value = raw[0]  # list with one tuple
    number = value[0]
    total = value[1]
    return NumberOfTotalValue(number, total)


def _to_mp4_cover(artwork: Artwork) -> mutagen.mp4.MP4Cover:
    try:
        image_format = MP4_COVER_FORMAT_MAPPING[artwork.mime_type]
    except KeyError:
        raise ApitError(f"Unknown artwork mime type: {artwork.mime_type}")
    else:
        return mutagen.mp4.MP4Cover(artwork.content, imageformat=image_format)


def _encode_artwork(_: TagIdEnum, __: Song, artwork: Artwork | None) -> list | None:
    if artwork is None:
        return None
    # TODO first, remove all artwork
    return [_to_mp4_cover(artwork)]


# Writable fields come first, in the order they are written.
MP4_FIELDS: Final[tuple[Field, ...]] = (
    Field(TagName.ARTIST, Mp4Mapping.ARTIST, encode=lambda _, s, a: s.artist),
    Field(TagName.TITLE, Mp4Mapping.TITLE, encode=lambda _, s, a: s.title),
    Field(
        TagName.ALBUM_NAME,
        Mp4Mapping.ALBUM_NAME,
        encode=lambda _, s, a: s.album_name,
    ),
    Field(TagName.GENRE, Mp4Mapping.GENRE, encode=lambda _, s, a: s.genre),
    Field(
        TagName.RELEASE_DATE,
        Mp4Mapping.RELEASE_DATE,
        encode=lambda _, s, a: s.release_date,
    ),
    Field(
        TagName.DISC_NUMBER,
        Mp4Mapping.DISC_NUMBER,
        _decode_number_of_total,
        lambda _, s, a: [(s.disc_number, s.disc_total)],
    ),
    Field(
        TagName.TRACK_NUMBER,
        Mp4Mapping.TRACK_NUMBER,
        _decode_number_of_total,
        lambda _, s, a: [(s.track_number, s.track_total)],
    ),
    Field(
        TagName.RATING,
        Mp4Mapping.RATING,
        _decode_rating,
        lambda _, s, a: [RATING_MAPPING[s.rating]],
    ),
    Field(
        TagName.MEDIA_TYPE,
        Mp4Mapping.MEDIA_TYPE,
        _decode_media_kind,
        lambda _, s, a: [ITEM_KIND_MAPPING[s.media_kind]],
    ),
    Field(
        TagName.ALBUM_ARTIST,
        Mp4Mapping.ALBUM_ARTIST,
        encode=lambda _, s, a: s.album_artist,
    ),
    Field(
        TagName.COPYRIGHT,
        Mp4Mapping.COPYRIGHT,
        encode=lambda _, s, a: s.copyright,
    ),
    Field(
        TagName.COMPILATION,
        Mp4Mapping.COMPILATION,
        _decode_flag,
        lambda _, s, a: s.compilation,
    ),
    Field(
        TagName.CONTENT_ID,
        Mp4Mapping.CONTENT_ID,
        encode=lambda _, s, a: [s.content_id],
    ),
    Field(TagName.ARTWORK, Mp4Mapping.ARTWORK, _decode_artwork, _encode_artwork),
    # read-only fields
    Field(TagName.GAPLESS, Mp4Mapping.GAPLESS, _decode_flag),
    Field(TagName.LYRICS, Mp4Mapping.LYRICS, _decode_lyrics),
    Field(TagName.COMPOSER, Mp4Mapping.COMPOSER),
    Field(TagName.SORT_ORDER_TITLE, Mp4Mapping.SORT_ORDER_TITLE),
    Field(TagName.SORT_ORDER_ARTIST, Mp4Mapping.SORT_ORDER_ARTIST),
    Field(TagName.SORT_ORDER_ALBUM, Mp4Mapping.SORT_ORDER_ALBUM),
    Field(
        TagName.SORT_ORDER_ALBUM_ARTIST,
        Mp4Mapping.SORT_ORDER_ALBUM_ARTIST,
    ),
    Field(TagName.SORT_ORDER_COMPOSER, Mp4Mapping.SORT_ORDER_COMPOSER),
    Field(TagName.GROUPING, Mp4Mapping.GROUPING),
    Field(TagName.COMMENT, Mp4Mapping.COMMENT),
    Field(TagName.BPM, Mp4Mapping.BPM),
    Field(TagName.TOOL, Mp4Mapping.TOOL),
    Field(TagName.PLAYLIST_ID, Mp4Mapping.PLAYLIST_ID),
    Field(TagName.ARTIST_ID, Mp4Mapping.ARTIST_ID),
    Field(TagName.GENRE_ID, Mp4Mapping.GENRE_ID),
    Field(TagName.COMPOSER_ID, Mp4Mapping.COMPOSER_ID),
    Field(TagName.ISRC_ID, Mp4Mapping.ISRC_ID),
    Field(TagName.OWNER_NAME, Mp4Mapping.OWNER_NAME),
    Field(TagName.USER_MAIL, Mp4Mapping.USER_MAIL),
    Field(TagName.PURCHASE_DATE, Mp4Mapping.PURCHASE_DATE),
    Field(TagName.STOREFRONT_ID, Mp4Mapping.STOREFRONT_ID),
)

MP4_FIELDS_BY_ID: Final[Mapping[str, Field]] = {
    field.tag_id.value: field for field in MP4_FIELDS
}
