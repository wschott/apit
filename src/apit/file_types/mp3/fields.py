from collections.abc import Callable
from collections.abc import Mapping
from collections.abc import Sequence
from datetime import datetime
from typing import Any
from typing import Final

import mutagen.id3
from mutagen.id3 import Encoding

from .constants import Mp3Mapping
from apit.core.audio.tag_id import TagIdEnum
from apit.core.audio.tag_name import TagName
from apit.core.audio.tag_value import ArtworkValue
from apit.core.audio.tag_value import FlagValue
from apit.core.audio.tag_value import LyricsValue
from apit.core.audio.tag_value import TagValue
from apit.core.audio.tag_value import TextValue
from apit.core.metadata.artwork import Artwork
from apit.core.metadata.song import Song
from apit.file_types.field import Field

type Id3FrameEncoder = Callable[
    [TagIdEnum, Song, Artwork | None], Sequence[mutagen.id3.Frame] | None
]


def _decode_flag(raw: Any) -> TagValue:
    return FlagValue(raw.text[0] == "1")


def _decode_lyrics(raw: Any) -> TagValue:
    return LyricsValue(raw.text)


def _decode_artwork(raw: Any) -> TagValue:
    return ArtworkValue(None)


def decode_default(raw: Any) -> TagValue:
    if isinstance(raw, mutagen.id3.USLT):
        return _decode_lyrics(raw)
    if isinstance(raw, mutagen.id3.APIC):
        return _decode_artwork(raw)
    if isinstance(raw, mutagen.id3.TCMP):
        return _decode_flag(raw)
    return TextValue(str(raw))


def extract_year(date: str) -> str:
    return str(datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").year)


def id3_text_frame(tag_id: TagIdEnum, value: str) -> mutagen.id3.TextFrame:
    return mutagen.id3.Frames[tag_id](encoding=Encoding.UTF8, text=value)


def _text(value: Callable[[Song], str]) -> Id3FrameEncoder:
    return lambda tag_id, song, _: [id3_text_frame(tag_id, value(song))]


def _encode_compilation(
    tag_id: TagIdEnum, song: Song, _: Artwork | None
) -> list[mutagen.id3.Frame]:
    if song.compilation:
        return [id3_text_frame(tag_id, str(int(song.compilation)))]
    return []


def _encode_artwork(
    _: TagIdEnum, __: Song, artwork: Artwork | None
) -> list[mutagen.id3.APIC] | None:
    if artwork is None:
        return None
    return [
        mutagen.id3.APIC(
            mime=artwork.mime_type.value,
            type=mutagen.id3.PictureType.COVER_FRONT,
            data=artwork.content,
        )
    ]


# Writable fields come first, in the order they are written. Rating, media
# type and content ID are not written (nor read by name) for mp3.
MP3_FIELDS: Final[tuple[Field, ...]] = (
    Field(
        TagName.ARTIST,
        Mp3Mapping.ARTIST,
        encode=_text(lambda s: s.artist),
    ),
    Field(
        TagName.TITLE,
        Mp3Mapping.TITLE,
        encode=_text(lambda s: s.title),
    ),
    Field(
        TagName.ALBUM_NAME,
        Mp3Mapping.ALBUM_NAME,
        encode=_text(lambda s: s.album_name),
    ),
    Field(
        TagName.GENRE,
        Mp3Mapping.GENRE,
        encode=_text(lambda s: s.genre),
    ),
    Field(
        TagName.RELEASE_DATE,
        Mp3Mapping.RELEASE_DATE,
        encode=_text(lambda s: extract_year(s.release_date)),
    ),
    Field(
        TagName.DISC_NUMBER,
        Mp3Mapping.DISC_NUMBER,
        encode=_text(lambda s: f"{s.disc_number}/{s.disc_total}"),
    ),
    Field(
        TagName.TRACK_NUMBER,
        Mp3Mapping.TRACK_NUMBER,
        encode=_text(lambda s: f"{s.track_number}/{s.track_total}"),
    ),
    Field(
        TagName.ALBUM_ARTIST,
        Mp3Mapping.ALBUM_ARTIST,
        encode=_text(lambda s: s.album_artist),
    ),
    Field(
        TagName.COPYRIGHT,
        Mp3Mapping.COPYRIGHT,
        encode=_text(lambda s: s.copyright),
    ),
    Field(
        TagName.COMPILATION, Mp3Mapping.COMPILATION, _decode_flag, _encode_compilation
    ),
    Field(TagName.ARTWORK, Mp3Mapping.ARTWORK, _decode_artwork, _encode_artwork),
    # read-only fields
    Field(TagName.GAPLESS, Mp3Mapping.GAPLESS, _decode_flag),
    Field(TagName.LYRICS, Mp3Mapping.LYRICS, _decode_lyrics),
    Field(TagName.COMPOSER, Mp3Mapping.COMPOSER),
    Field(TagName.SORT_ORDER_TITLE, Mp3Mapping.SORT_ORDER_TITLE),
    Field(TagName.SORT_ORDER_ARTIST, Mp3Mapping.SORT_ORDER_ARTIST),
    Field(TagName.SORT_ORDER_ALBUM, Mp3Mapping.SORT_ORDER_ALBUM),
    Field(
        TagName.SORT_ORDER_ALBUM_ARTIST,
        Mp3Mapping.SORT_ORDER_ALBUM_ARTIST,
    ),
    Field(TagName.SORT_ORDER_COMPOSER, Mp3Mapping.SORT_ORDER_COMPOSER),
    # TODO Field(TagName.ISRC_ID, Mp3Mapping.ISRC_ID),
    Field(TagName.GROUPING, Mp3Mapping.GROUPING),
    Field(TagName.COMMENT, Mp3Mapping.COMMENT),
    Field(TagName.BPM, Mp3Mapping.BPM),
    Field(TagName.TOOL, Mp3Mapping.TOOL),
)

MP3_FIELDS_BY_ID: Final[Mapping[str, Field]] = {
    field.tag_id.value: field for field in MP3_FIELDS
}
