from collections.abc import Mapping

from apit.store.constants import ITEM_KIND_MAPPING
from apit.store.constants import MP4_MAPPING
from apit.store.constants import RATING_MAPPING
from apit.store.constants import STORE_KIND
from apit.store.constants import STORE_RATING

MP4_MAPPING_TO_HUMAN_READABLE: Mapping[MP4_MAPPING, str] = {
    MP4_MAPPING.TITLE: "Title",
    MP4_MAPPING.ARTIST: "Artist",
    MP4_MAPPING.ALBUM_NAME: "Album",
    MP4_MAPPING.ALBUM_ARTIST: "Album Artist",
    MP4_MAPPING.COMPOSER: "Composer",
    MP4_MAPPING.SORT_ORDER_TITLE: "Sort Title",
    MP4_MAPPING.SORT_ORDER_ARTIST: "Sort Artist",
    MP4_MAPPING.SORT_ORDER_ALBUM: "Sort Album",
    MP4_MAPPING.SORT_ORDER_ALBUM_ARTIST: "Sort Album Artist",
    MP4_MAPPING.SORT_ORDER_COMPOSER: "Sort Composer",
    MP4_MAPPING.TRACK_NUMBER: "Track #/Total",
    MP4_MAPPING.DISC_NUMBER: "Disc #/Total",
    MP4_MAPPING.GENRE: "Genre",
    MP4_MAPPING.RELEASE_DATE: "Date",
    MP4_MAPPING.COPYRIGHT: "Copyright",
    MP4_MAPPING.COMPILATION: "Compilation?",
    MP4_MAPPING.GAPLESS: "Gapless?",
    MP4_MAPPING.RATING: "Rating",
    MP4_MAPPING.MEDIA_TYPE: "Media Type",
    MP4_MAPPING.CONTENT_ID: "Content ID",
    MP4_MAPPING.PLAYLIST_ID: "Playlist ID",
    MP4_MAPPING.ARTIST_ID: "Artist ID",
    MP4_MAPPING.GENRE_ID: "Genre ID",
    MP4_MAPPING.COMPOSER_ID: "Composer ID",
    MP4_MAPPING.ISRC_ID: "ISRC",
    MP4_MAPPING.GROUPING: "Grouping",
    MP4_MAPPING.COMMENT: "Comment",
    MP4_MAPPING.ARTWORK: "Artwork",
    MP4_MAPPING.BPM: "BPM",
    MP4_MAPPING.TOOL: "Tool",
    MP4_MAPPING.LYRICS: "Lyrics",
    MP4_MAPPING.OWNER_NAME: "Owner",
    MP4_MAPPING.USER_MAIL: "Email",
    MP4_MAPPING.PURCHASE_DATE: "Purchase Date",
    MP4_MAPPING.STOREFRONT_ID: "Storefront ID",
}
RATING_TO_HUMAN_READABLE: Mapping[int, str] = {
    4: "<explicit (old value)>",  # TODO
    RATING_MAPPING[STORE_RATING.CLEAN]: "<clean>",
    RATING_MAPPING[STORE_RATING.EXPLICIT]: "<explicit>",
    RATING_MAPPING[STORE_RATING.NONE]: "<inoffensive>",
}
MEDIA_TYPE_TO_HUMAN_READABLE: Mapping[int, str] = {
    ITEM_KIND_MAPPING[STORE_KIND.SONG]: "<normal>",
}
