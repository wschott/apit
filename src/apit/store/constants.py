# flake8: noqa

# Documentation:
# https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
# https://godoc.org/trimmer.io/go-xmp/models/itunes

from collections.abc import Mapping
from enum import Enum

from apit.error import ApitError

COLLECTION_TYPE_KEY = "collectionType"
VALID_COLLECTION_TYPE_FOR_ALBUM = "Album"
KIND_KEY = "kind"
VALID_KIND_VALUES_FOR_SONG = "song"


class STORE_KEY(Enum):
    # song values
    ARTIST          = 'artistName'
    TITLE           = 'trackCensoredName'  # alternatively: 'trackName' without stars '*'
    ALBUM_NAME      = 'collectionCensoredName'  # alternatively: 'collectionName' without stars '*'; in ALBUM: both fields are present as well
    GENRE           = 'primaryGenreName'
    RELEASE_DATE    = 'releaseDate'
    TRACK_NUMBER    = 'trackNumber'
    TRACK_TOTAL     = 'trackCount'
    DISC_NUMBER     = 'discNumber'
    DISC_TOTAL      = 'discCount'
    RATING          = 'trackExplicitness'
    MEDIA_KIND      = 'kind'
    CONTENT_ID      = 'trackId'  # catalog ID
    COLLECTION_ID   = 'collectionId'  # same as ALBUM:collectionId   # TODO rename to PLAYLIST_ID?
    COLLECTION_ARTIST = 'collectionArtistName'  # presence indicates, that this is part of a compilation
    # TODO ARTIST_ID       = 'artistId'

    # album values
    ALBUM_ARTIST    = 'artistName'
    COPYRIGHT       = 'copyright'
    ARTWORK_URL     = 'artworkUrl100'


class STORE_RATING(Enum):
    CLEAN    = 'cleaned'
    EXPLICIT = 'explicit'
    NONE     = 'notExplicit'
    #EXPLICIT_OLD = 'explicit'


RATING_MAPPING: Mapping[STORE_RATING, int] = {
    # itunes value -> mutagen value
    STORE_RATING.CLEAN: 2,
    STORE_RATING.EXPLICIT: 1,
    STORE_RATING.NONE: 0,

    #STORE_RATING.EXPLICIT_OLD: 4,  # TODO
}


def to_rating(rating_str: str) -> STORE_RATING:
    try:
        return STORE_RATING(rating_str)
    except ValueError as e:
        raise ApitError("[Error] Unknown rating: %s" % e)


class STORE_KIND(Enum):
    ALBUM = "album"
    SONG = "song"


ITEM_KIND_MAPPING: Mapping[STORE_KIND, int] = {
    # itunes value -> mutagen value
    STORE_KIND.SONG: 1,
}


def to_item_kind(kind_str: str) -> STORE_KIND:
    try:
        return STORE_KIND(kind_str)
    except ValueError as e:
        raise ApitError("[Error] Unknown item kind: %s" % e)


# https://affiliate.itunes.apple.com/resources/documentation/genre-mapping/
# https://itunes.apple.com/WebObjects/MZStoreServices.woa/ws/genres
# GENRE_MAP = {
#     'African': 1203,
#     'Alternative': 20,
#     'Arabic': 1197,
#     'Blues': 2,
#     'Brazilian': 1122,
#     "Children's Music": 4,
#     'Christian & Gospel': 22,
#     'Classical': 5,
#     'Comedy': 3,
#     'Country': 6,
#     'Dance': 17,
#     'Easy Listening': 25,
#     'Electronic': 7,
#     'Fitness & Workout': 50,
#     'Folk': 1289,
#     'French Pop': 50000064,
#     'Hip-Hop/Rap': 18,
#     'Holiday': 8,
#     'Christian & Gospel': 100000,
#     'Instrumental': 53,
#     'J-Pop': 27,
#     'Jazz': 11,
#     'Korean': 1243,
#     'Latino': 12,
#     'New Age': 13,
#     'Orchestral': 1290,
#     'Pop': 14,
#     'R&B/Soul': 15,
#     'Reggae': 24,
#     'Rock': 21,
#     'Russian': 1299,
#     'Singer/Songwriter': 10,
#     'Soundtrack': 16,
#     'Turkish': 1300,
#     'Vocal': 23,
#     'World': 19
# }

# Atom meanings: see https://github.com/quodlibet/mutagen/blob/master/mutagen/mp4/__init__.py
class MP4_MAPPING(Enum):
    TITLE           = '\xa9nam'
    ALBUM_NAME      = '\xa9alb'
    ARTIST          = '\xa9ART'
    ALBUM_ARTIST    = 'aART'
    RELEASE_DATE    = '\xa9day'
    GENRE           = '\xa9gen'
    COPYRIGHT       = 'cprt'
    TRACK_NUMBER    = 'trkn'
    DISC_NUMBER     = 'disk'
    RATING          = 'rtng'  # TODO int
    MEDIA_TYPE      = 'stik'  # TODO int
    CONTENT_ID      = 'cnID'  # catalog ID
    COMPILATION     = 'cpil'  # bool
    ARTWORK         = 'covr'

    OWNER_NAME      = 'ownr'
    USER_MAIL       = 'apID'

    # TODO unused for now
    GAPLESS         = 'pgap'
    BPM             = 'tmpo'
    COMPOSER        = '\xa9wrt'
    COMMENT         = '\xa9cmt'
    GROUPING        = '\xa9grp'
    TOOL            = '\xa9too'
    LYRICS          = '\xa9lyr'
    PURCHASE_DATE   = 'purd'

    PLAYLIST_ID     = 'plID'
    ARTIST_ID       = 'atID'
    GENRE_ID        = 'geID'
    COMPOSER_ID     = 'cmID'  # really composer id?
    ISRC_ID         = 'xid '  # yes, with a space at the end; mixture of "{Record_Label_Name}:isrc:{ISRC_SONG_CODE}"
    STOREFRONT_ID   = 'sfID'

    SORT_ORDER_TITLE = 'sonm'
    SORT_ORDER_ARTIST = 'soar'
    SORT_ORDER_ALBUM = 'soal'
    SORT_ORDER_ALBUM_ARTIST = 'soaa'
    SORT_ORDER_COMPOSER = 'soco'

BLACKLIST: list[str] = [
    MP4_MAPPING.OWNER_NAME.value,
    MP4_MAPPING.USER_MAIL.value,
]
