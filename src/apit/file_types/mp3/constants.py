# ruff: noqa
from apit.tag_id import TagIdEnum


# Atom meanings: see https://github.com/quodlibet/mutagen/blob/master/mutagen/id3/_frames.py
class Mp3Mapping(TagIdEnum):
    TITLE = "TIT2"
    ALBUM_NAME = "TALB"
    ARTIST = "TPE1"
    ALBUM_ARTIST = "TPE2"
    RELEASE_DATE = "TDRC"
    GENRE = "TCON"
    COPYRIGHT = "TCOP"
    TRACK_NUMBER = "TRCK"
    DISC_NUMBER = "TPOS"
    COMPILATION = "TCMP"
    ARTWORK = "APIC:"

    GAPLESS = "COMM:iTunPGAP:eng"  # TODO verify with frame class
    BPM = "TBPM"
    COMPOSER = "TCOM"
    COMMENT = "COMM::eng"
    GROUPING = "GRP1"
    TOOL = "TENC"
    LYRICS = "USLT::eng"

    SORT_ORDER_TITLE = "TSOT"
    SORT_ORDER_ARTIST = "TSOP"
    SORT_ORDER_ALBUM = "TSOA"
    SORT_ORDER_ALBUM_ARTIST = "TSO2"
    SORT_ORDER_COMPOSER = "TSOC"

    ISRC_ID = "TSRC"
