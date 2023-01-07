from collections.abc import Mapping

from apit.store.constants import ITEM_KIND_MAPPING
from apit.store.constants import RATING_MAPPING
from apit.store.constants import STORE_KIND
from apit.store.constants import STORE_RATING
from apit.str_enum import StrEnum


class ReadableTagName(StrEnum):
    TITLE = "Title"
    ARTIST = "Artist"
    ALBUM_NAME = "Album"
    ALBUM_ARTIST = "Album Artist"
    COMPOSER = "Composer"
    SORT_ORDER_TITLE = "Sort Title"
    SORT_ORDER_ARTIST = "Sort Artist"
    SORT_ORDER_ALBUM = "Sort Album"
    SORT_ORDER_ALBUM_ARTIST = "Sort Album Artist"
    SORT_ORDER_COMPOSER = "Sort Composer"
    TRACK_NUMBER = "Track #/Total"
    DISC_NUMBER = "Disc #/Total"
    GENRE = "Genre"
    RELEASE_DATE = "Date"
    COPYRIGHT = "Copyright"
    COMPILATION = "Compilation?"
    GAPLESS = "Gapless?"
    RATING = "Rating"
    MEDIA_TYPE = "Media Type"
    CONTENT_ID = "Content ID"
    PLAYLIST_ID = "Playlist ID"
    ARTIST_ID = "Artist ID"
    GENRE_ID = "Genre ID"
    COMPOSER_ID = "Composer ID"
    ISRC_ID = "ISRC"
    GROUPING = "Grouping"
    COMMENT = "Comment"
    ARTWORK = "Artwork"
    BPM = "BPM"
    TOOL = "Tool"
    LYRICS = "Lyrics"
    OWNER_NAME = "Owner"
    USER_MAIL = "Email"
    PURCHASE_DATE = "Purchase Date"
    STOREFRONT_ID = "Storefront ID"


RATING_TO_READABLE_NAME: Mapping[int, str] = {
    4: "<explicit (old value)>",  # TODO
    RATING_MAPPING[STORE_RATING.CLEAN]: "<clean>",
    RATING_MAPPING[STORE_RATING.EXPLICIT]: "<explicit>",
    RATING_MAPPING[STORE_RATING.NONE]: "<inoffensive>",
}
MEDIA_TYPE_TO_READABLE_NAME: Mapping[int, str] = {
    ITEM_KIND_MAPPING[STORE_KIND.SONG]: "<normal>",
}
