# flake8: noqa
# Documentation:
# https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
# https://godoc.org/trimmer.io/go-xmp/models/itunes
from enum import Enum
from enum import StrEnum
from typing import Final

from apit.errors import ApitError

COLLECTION_TYPE_KEY: Final = "collectionType"
VALID_COLLECTION_TYPE_FOR_ALBUM: Final = "Album"
KIND_KEY: Final = "kind"
VALID_KIND_VALUES_FOR_SONG: Final = "song"


class StoreKey(StrEnum):
    # song values
    ARTIST = "artistName"
    TITLE = "trackCensoredName"  # alternatively: 'trackName' without stars '*'
    ALBUM_NAME = "collectionCensoredName"  # alternatively: 'collectionName' without stars '*'; in ALBUM: both fields are present as well
    GENRE = "primaryGenreName"
    RELEASE_DATE = "releaseDate"
    TRACK_NUMBER = "trackNumber"
    TRACK_TOTAL = "trackCount"
    DISC_NUMBER = "discNumber"
    DISC_TOTAL = "discCount"
    RATING = "trackExplicitness"
    MEDIA_KIND = "kind"
    CONTENT_ID = "trackId"  # catalog ID
    COLLECTION_ID = (
        "collectionId"  # same as ALBUM:collectionId   # TODO rename to PLAYLIST_ID?
    )
    COLLECTION_ARTIST = (
        "collectionArtistId"  # presence indicates, that this is part of a compilation
    )
    # TODO ARTIST_ID       = 'artistId'

    # album values
    ALBUM_ARTIST = "artistName"
    COPYRIGHT = "copyright"
    ARTWORK_URL = "artworkUrl100"


class StoreRating(Enum):
    CLEAN = "cleaned"
    EXPLICIT = "explicit"
    NONE = "notExplicit"
    # EXPLICIT_OLD = 'explicit'


RATING_MAPPING: Final[dict[StoreRating, int]] = {
    # itunes value -> mutagen value
    StoreRating.CLEAN: 2,
    StoreRating.EXPLICIT: 1,
    StoreRating.NONE: 0,
    # STORE_RATING.EXPLICIT_OLD: 4,  # TODO
}


def to_rating(rating_str: str) -> StoreRating:
    try:
        return StoreRating(rating_str)
    except ValueError as e:
        raise ApitError("[Error] Unknown rating: %s" % e)


class StoreKind(Enum):
    ALBUM = "album"
    SONG = "song"


ITEM_KIND_MAPPING: Final[dict[StoreKind, int]] = {
    # itunes value -> mutagen value
    StoreKind.SONG: 1,
}


def to_item_kind(kind_str: str) -> StoreKind:
    try:
        return StoreKind(kind_str)
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
