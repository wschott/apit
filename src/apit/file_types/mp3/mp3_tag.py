import os

import mutagen.id3

from .constants import Mp3Mapping
from apit.readable_names import ReadableTagName
from apit.tag_id import TagId
from apit.tagged_value import TaggedValue


class Mp3Tag(TaggedValue):
    def _get_readable_name(self, tag_id: TagId) -> ReadableTagName | None:
        try:
            mapped_tag_id = Mp3Mapping(tag_id)
            return MP3_MAPPING_TO_READABLE_TAG_NAME.get(mapped_tag_id)
        except ValueError:
            return None

    def value(self, verbose: bool) -> str:
        if isinstance(self._unprocessed_value, mutagen.id3.USLT):  # MP3_MAPPING.LYRICS
            lyrics = self._unprocessed_value
            if verbose:
                return lyrics.text.replace("\r", os.linesep)  # type: ignore[attr-defined]
            return "<present>"
        elif isinstance(
            self._unprocessed_value, mutagen.id3.APIC
        ):  # MP3_MAPPING.ARTWORK
            return "<present>"
        elif self.tag_id == Mp3Mapping.GAPLESS or isinstance(
            self._unprocessed_value,
            mutagen.id3.TCMP,  # MP3_MAPPING.COMPILATION
        ):
            return "<yes>" if self._unprocessed_value.text[0] == "1" else "<no>"
        else:
            return str(self._unprocessed_value)


MP3_MAPPING_TO_READABLE_TAG_NAME: dict[Mp3Mapping, ReadableTagName] = {
    Mp3Mapping.TITLE: ReadableTagName.TITLE,
    Mp3Mapping.ARTIST: ReadableTagName.ARTIST,
    Mp3Mapping.ALBUM_NAME: ReadableTagName.ALBUM_NAME,
    Mp3Mapping.ALBUM_ARTIST: ReadableTagName.ALBUM_ARTIST,
    Mp3Mapping.COMPOSER: ReadableTagName.COMPOSER,
    Mp3Mapping.SORT_ORDER_TITLE: ReadableTagName.SORT_ORDER_TITLE,
    Mp3Mapping.SORT_ORDER_ARTIST: ReadableTagName.SORT_ORDER_ARTIST,
    Mp3Mapping.SORT_ORDER_ALBUM: ReadableTagName.SORT_ORDER_ALBUM,
    Mp3Mapping.SORT_ORDER_ALBUM_ARTIST: ReadableTagName.SORT_ORDER_ALBUM_ARTIST,
    Mp3Mapping.SORT_ORDER_COMPOSER: ReadableTagName.SORT_ORDER_COMPOSER,
    Mp3Mapping.TRACK_NUMBER: ReadableTagName.TRACK_NUMBER,
    Mp3Mapping.DISC_NUMBER: ReadableTagName.DISC_NUMBER,
    Mp3Mapping.GENRE: ReadableTagName.GENRE,
    Mp3Mapping.RELEASE_DATE: ReadableTagName.RELEASE_DATE,
    Mp3Mapping.COPYRIGHT: ReadableTagName.COPYRIGHT,
    Mp3Mapping.COMPILATION: ReadableTagName.COMPILATION,
    # TODO MP3_MAPPING.ISRC_ID: ReadableTagName.ISRC_ID,
    Mp3Mapping.GROUPING: ReadableTagName.GROUPING,
    Mp3Mapping.COMMENT: ReadableTagName.COMMENT,
    Mp3Mapping.ARTWORK: ReadableTagName.ARTWORK,
    Mp3Mapping.LYRICS: ReadableTagName.LYRICS,
    Mp3Mapping.BPM: ReadableTagName.BPM,
    Mp3Mapping.TOOL: ReadableTagName.TOOL,
    Mp3Mapping.GAPLESS: ReadableTagName.GAPLESS,
}
