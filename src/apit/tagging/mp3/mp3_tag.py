import os
from collections.abc import Mapping

import mutagen.id3

from .constants import MP3_MAPPING
from apit.readable_names import ReadableTagName
from apit.tag_id import TagId
from apit.tagged_value import TaggedValue


class Mp3Tag(TaggedValue):
    def _get_readable_name(self, tag_id: TagId) -> ReadableTagName | None:
        try:
            mapped_tag_id = MP3_MAPPING(tag_id)
            return MP3_MAPPING_TO_READABLE_TAG_NAME.get(mapped_tag_id, None)
        except ValueError:
            return None

    def value(self, verbose: bool) -> str:
        if isinstance(self._unprocessed_value, mutagen.id3.USLT):  # MP3_MAPPING.LYRICS
            lyrics = self._unprocessed_value
            if verbose:
                return lyrics.text.replace("\r", os.linesep)  # type: ignore
            return "<present>"
        elif isinstance(
            self._unprocessed_value, mutagen.id3.APIC
        ):  # MP3_MAPPING.ARTWORK
            return "<present>"
        elif isinstance(
            self._unprocessed_value, mutagen.id3.TCMP
        ):  # MP3_MAPPING.COMPILATION
            return "<yes>" if self._unprocessed_value.text[0] == "1" else "<no>"  # type: ignore
        else:
            return self._unprocessed_value


MP3_MAPPING_TO_READABLE_TAG_NAME: Mapping[MP3_MAPPING, ReadableTagName] = {
    MP3_MAPPING.TITLE: ReadableTagName.TITLE,
    MP3_MAPPING.ARTIST: ReadableTagName.ARTIST,
    MP3_MAPPING.ALBUM_NAME: ReadableTagName.ALBUM_NAME,
    MP3_MAPPING.ALBUM_ARTIST: ReadableTagName.ALBUM_ARTIST,
    MP3_MAPPING.COMPOSER: ReadableTagName.COMPOSER,
    MP3_MAPPING.SORT_ORDER_TITLE: ReadableTagName.SORT_ORDER_TITLE,
    MP3_MAPPING.SORT_ORDER_ARTIST: ReadableTagName.SORT_ORDER_ARTIST,
    MP3_MAPPING.SORT_ORDER_ALBUM: ReadableTagName.SORT_ORDER_ALBUM,
    MP3_MAPPING.SORT_ORDER_ALBUM_ARTIST: ReadableTagName.SORT_ORDER_ALBUM_ARTIST,
    MP3_MAPPING.SORT_ORDER_COMPOSER: ReadableTagName.SORT_ORDER_COMPOSER,
    MP3_MAPPING.TRACK_NUMBER: ReadableTagName.TRACK_NUMBER,
    MP3_MAPPING.DISC_NUMBER: ReadableTagName.DISC_NUMBER,
    MP3_MAPPING.GENRE: ReadableTagName.GENRE,
    MP3_MAPPING.RELEASE_DATE: ReadableTagName.RELEASE_DATE,
    MP3_MAPPING.COPYRIGHT: ReadableTagName.COPYRIGHT,
    MP3_MAPPING.COMPILATION: ReadableTagName.COMPILATION,
    # TODO MP3_MAPPING.ISRC_ID: ReadableTagName.ISRC_ID,
    MP3_MAPPING.GROUPING: ReadableTagName.GROUPING,
    MP3_MAPPING.COMMENT: ReadableTagName.COMMENT,
    MP3_MAPPING.ARTWORK: ReadableTagName.ARTWORK,
    MP3_MAPPING.LYRICS: ReadableTagName.LYRICS,
    MP3_MAPPING.BPM: ReadableTagName.BPM,
    MP3_MAPPING.TOOL: ReadableTagName.TOOL,
    MP3_MAPPING.GAPLESS: ReadableTagName.GAPLESS,
}
