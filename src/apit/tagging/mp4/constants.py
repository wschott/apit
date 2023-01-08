# flake8: noqa
from apit.tag_id import TagIdEnum


# Atom meanings: see https://github.com/quodlibet/mutagen/blob/master/mutagen/mp4/__init__.py
class MP4_MAPPING(TagIdEnum):
    # fmt: off
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
    # fmt: on