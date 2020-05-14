# flake8: noqa

# Documentation:
# https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/

from enum import Enum

from apit.error import ApitError

COLLECTION_TYPE_KEY = 'collectionType'
VALID_COLLECTION_TYPE_VALUES_FOR_ALBUMS = ['Album', 'Compilation']
KIND_KEY = 'kind'
VALID_KIND_VALUES_FOR_SONG = 'song'


class STORE_KEY(Enum):
    # song values
    ARTIST          = 'artistName'
    TITLE           = 'trackCensoredName'  # alternatively: 'trackName' without stars '*'
    ALBUM_NAME      = 'collectionCensoredName'  # alternatively: 'collectionName' without stars '*'; in ALBUM: both fields are present as well
    GENRE           = 'primaryGenreName'
    YEAR            = 'releaseDate'
    TRACK_NUMBER    = 'trackNumber'
    TRACK_TOTAL     = 'trackCount'
    DISC_NUMBER     = 'discNumber'
    DISC_TOTAL      = 'discCount'
    RATING          = 'trackExplicitness'
    MEDIA_KIND      = 'kind'
    CONTENT_ID      = 'trackId'
    COLLECTION_ID   = 'collectionId'  # same as ALBUM:collectionId   # TODO rename to PLAYLIST_ID?

    # TODO ARTIST_ID       = 'artistId'

    # album values
    ALBUM_ARTIST    = 'artistName'  # TODO sometimes (e.g. for compilations there is a 'Song:collectionArtistName' field
    COPYRIGHT       = 'copyright'

    # TODO ARTWORK_URL_100 = (METADATA_SOURCE.ALBUM, 'artworkUrl100')  # TODO change to 600x600, download and save to file


class STORE_RATING(Enum):
    CLEAN    = 'cleaned'
    EXPLICIT = 'explicit'
    NONE     = 'notExplicit'


AP_RATING_MAPPING = {
    # itunes value -> atomicparsley value
    STORE_RATING.CLEAN: 'clean',
    STORE_RATING.EXPLICIT: 'explicit',
    STORE_RATING.NONE: 'remove',
}


def to_rating(rating_str):
    try:
        return STORE_RATING(rating_str)
    except ValueError as e:
        raise ApitError('[Error] Unknown rating: %s' % e)


class STORE_KIND(Enum):
    ALBUM = 'album'
    SONG  = 'song'


AP_ITEM_KIND_MAPPING = {
    # itunes value -> atomicparsley value
    STORE_KIND.SONG: 'Normal',
}


def to_item_kind(kind_str):
    try:
        return STORE_KIND(kind_str)
    except ValueError as e:
        raise ApitError('[Error] Unknown item kind: %s' % e)


# https://affiliate.itunes.apple.com/resources/documentation/genre-mapping/
# GENRE_MAP = {
#     'Hip Hop/Rap': 18,
#     'Hip-Hop/Rap': 18,
#     'Dance': 17,
#     'Rock': 21,
# }

# class MP4_MAPPING(Enum):
#     TITLE           = '\xa9nam'
#     ALBUM           = '\xa9alb'
#     ARTIST          = '\xa9ART'
#     ALBUM_ARTIST    = 'aART'
#     YEAR            = '\xa9day'
#     GENRE           = '\xa9gen'
#     COPYRIGHT       = 'cprt'
#     TRACK_NUMBER    = 'trkn'
#     DISC_NUMBER     = 'disk'
#
#     RATING          = 'rtng'  # TODO int
#     MEDIA_KIND      = 'stik'  # TODO int
#
#     CONTENT_ID      = 'cnID'
#
#     # TODO unused for now
#     OWNER_NAME      = 'ownr'  # TODO use for blacklist
#     USER_MAIL       = 'apID'  # TODO use for blacklist
#
#     PLAYLIST_ID     = 'plID'
#     ARTIST_ID       = 'atID'
#     GENRE_ID        = 'geID'
#     STOREFRONT_ID   = 'sfID'
#     COMPOSER_ID     = 'cmID'  # really composer?
#     COMPILATION     = 'cpil'
#     PREGAP          = 'pgap'  # really pre gap?
#     UNKNOWN1        = 'akID'  # unknown id
#     UNKNOWN2        = 'xid '  # yes, with a space at the end; mixture of "{Record_Label_Name}:isrc:{ISRC_SONG_CODE}"
