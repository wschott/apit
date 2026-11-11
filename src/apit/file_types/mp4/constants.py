# ruff: noqa
from typing import Final

from apit.core.audio.tag_id import TagIdEnum
from apit.core.metadata.media_kind import MediaKind
from apit.core.metadata.rating import Rating


# Atom meanings: see https://github.com/quodlibet/mutagen/blob/master/mutagen/mp4/__init__.py
class Mp4Mapping(TagIdEnum):
    TITLE = "\xa9nam"
    ALBUM_NAME = "\xa9alb"
    ARTIST = "\xa9ART"
    ALBUM_ARTIST = "aART"
    RELEASE_DATE = "\xa9day"
    GENRE = "\xa9gen"
    COPYRIGHT = "cprt"
    TRACK_NUMBER = "trkn"
    DISC_NUMBER = "disk"
    COMPILATION = "cpil"  # bool
    ARTWORK = "covr"

    GAPLESS = "pgap"
    BPM = "tmpo"
    COMPOSER = "\xa9wrt"
    COMMENT = "\xa9cmt"
    GROUPING = "\xa9grp"
    TOOL = "\xa9too"
    LYRICS = "\xa9lyr"

    SORT_ORDER_TITLE = "sonm"
    SORT_ORDER_ARTIST = "soar"
    SORT_ORDER_ALBUM = "soal"
    SORT_ORDER_ALBUM_ARTIST = "soaa"
    SORT_ORDER_COMPOSER = "soco"

    # format specific values
    RATING = "rtng"  # TODO int
    MEDIA_TYPE = "stik"  # TODO int
    CONTENT_ID = "cnID"  # catalog ID
    OWNER_NAME = "ownr"
    USER_MAIL = "apID"
    PURCHASE_DATE = "purd"

    PLAYLIST_ID = "plID"
    ARTIST_ID = "atID"
    GENRE_ID = "geID"
    COMPOSER_ID = "cmID"  # really composer id?
    ISRC_ID = "xid "  # yes, with a space at the end; mixture of "{Record_Label_Name}:isrc:{ISRC_SONG_CODE}"
    STOREFRONT_ID = "sfID"


RATING_MAPPING: Final[dict[Rating, int]] = {
    # domain value -> mutagen value
    Rating.NONE: 0,
    Rating.EXPLICIT: 1,
    Rating.CLEAN: 2,
}


ITEM_KIND_MAPPING: Final[dict[MediaKind, int]] = {
    # domain value -> mutagen value
    MediaKind.SONG: 1,
}


RATING_FROM_MAPPING: Final[dict[int, Rating]] = {
    value: rating for rating, value in RATING_MAPPING.items()
}


ITEM_KIND_FROM_MAPPING: Final[dict[int, MediaKind]] = {
    value: kind for kind, value in ITEM_KIND_MAPPING.items()
}
