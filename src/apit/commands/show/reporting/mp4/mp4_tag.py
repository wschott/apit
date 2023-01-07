import os
from collections.abc import Mapping

from apit.commands.show.reporting.readable_names import MEDIA_TYPE_TO_READABLE_NAME
from apit.commands.show.reporting.readable_names import RATING_TO_READABLE_NAME
from apit.commands.show.reporting.readable_names import ReadableTagName
from apit.commands.show.reporting.tag_id_description import TagIdDescriptionValue
from apit.store.constants import MP4_MAPPING
from apit.tag_id import TagId


MP4_MAPPING_TO_READABLE_TAG_NAME: Mapping[MP4_MAPPING, ReadableTagName] = {
    MP4_MAPPING.TITLE: ReadableTagName.TITLE,
    MP4_MAPPING.ARTIST: ReadableTagName.ARTIST,
    MP4_MAPPING.ALBUM_NAME: ReadableTagName.ALBUM_NAME,
    MP4_MAPPING.ALBUM_ARTIST: ReadableTagName.ALBUM_ARTIST,
    MP4_MAPPING.COMPOSER: ReadableTagName.COMPOSER,
    MP4_MAPPING.SORT_ORDER_TITLE: ReadableTagName.SORT_ORDER_TITLE,
    MP4_MAPPING.SORT_ORDER_ARTIST: ReadableTagName.SORT_ORDER_ARTIST,
    MP4_MAPPING.SORT_ORDER_ALBUM: ReadableTagName.SORT_ORDER_ALBUM,
    MP4_MAPPING.SORT_ORDER_ALBUM_ARTIST: ReadableTagName.SORT_ORDER_ALBUM_ARTIST,
    MP4_MAPPING.SORT_ORDER_COMPOSER: ReadableTagName.SORT_ORDER_COMPOSER,
    MP4_MAPPING.TRACK_NUMBER: ReadableTagName.TRACK_NUMBER,
    MP4_MAPPING.DISC_NUMBER: ReadableTagName.DISC_NUMBER,
    MP4_MAPPING.GENRE: ReadableTagName.GENRE,
    MP4_MAPPING.RELEASE_DATE: ReadableTagName.RELEASE_DATE,
    MP4_MAPPING.COPYRIGHT: ReadableTagName.COPYRIGHT,
    MP4_MAPPING.COMPILATION: ReadableTagName.COMPILATION,
    MP4_MAPPING.GAPLESS: ReadableTagName.GAPLESS,
    MP4_MAPPING.RATING: ReadableTagName.RATING,
    MP4_MAPPING.MEDIA_TYPE: ReadableTagName.MEDIA_TYPE,
    MP4_MAPPING.CONTENT_ID: ReadableTagName.CONTENT_ID,
    MP4_MAPPING.PLAYLIST_ID: ReadableTagName.PLAYLIST_ID,
    MP4_MAPPING.ARTIST_ID: ReadableTagName.ARTIST_ID,
    MP4_MAPPING.GENRE_ID: ReadableTagName.GENRE_ID,
    MP4_MAPPING.COMPOSER_ID: ReadableTagName.COMPOSER_ID,
    MP4_MAPPING.ISRC_ID: ReadableTagName.ISRC_ID,
    MP4_MAPPING.GROUPING: ReadableTagName.GROUPING,
    MP4_MAPPING.COMMENT: ReadableTagName.COMMENT,
    MP4_MAPPING.ARTWORK: ReadableTagName.ARTWORK,
    MP4_MAPPING.BPM: ReadableTagName.BPM,
    MP4_MAPPING.TOOL: ReadableTagName.TOOL,
    MP4_MAPPING.LYRICS: ReadableTagName.LYRICS,
    MP4_MAPPING.OWNER_NAME: ReadableTagName.OWNER_NAME,
    MP4_MAPPING.USER_MAIL: ReadableTagName.USER_MAIL,
    MP4_MAPPING.PURCHASE_DATE: ReadableTagName.PURCHASE_DATE,
    MP4_MAPPING.STOREFRONT_ID: ReadableTagName.STOREFRONT_ID,
}


class Mp4Tag(TagIdDescriptionValue):
    def _get_readable_name(self, tag_id: TagId) -> ReadableTagName | None:
        try:
            mapped_tag_id = MP4_MAPPING(tag_id)
            return MP4_MAPPING_TO_READABLE_TAG_NAME.get(mapped_tag_id, None)
        except ValueError:
            return None

    def value(self, verbose: bool) -> str:
        if self.tag_id in [
            MP4_MAPPING.COMPILATION,
            MP4_MAPPING.GAPLESS,
        ]:  # no list
            return "<yes>" if self._unprocessed_value else "<no>"
        elif self.tag_id == MP4_MAPPING.RATING:  # list
            return RATING_TO_READABLE_NAME[int(self._unprocessed_value[0])]
        elif self.tag_id == MP4_MAPPING.MEDIA_TYPE:  # list
            return MEDIA_TYPE_TO_READABLE_NAME[self._unprocessed_value[0]]
        elif self.tag_id == MP4_MAPPING.LYRICS:  # list
            lyrics = self._unprocessed_value[0]
            if verbose:
                return lyrics.replace("\r", os.linesep)
            return "<present>"
        elif self.tag_id == MP4_MAPPING.ARTWORK:  # list
            return f"<{len(self._unprocessed_value)} present>"
        elif self.tag_id in [  # list with one tuple
            MP4_MAPPING.TRACK_NUMBER,
            MP4_MAPPING.DISC_NUMBER,
        ]:
            item = self._unprocessed_value[0][0] or "<none>"
            total_items = self._unprocessed_value[0][1] or "<none>"
            return f"{item}/{total_items}"

        elif isinstance(self._unprocessed_value, list):  # most mp4 tags
            return "".join([str(x) for x in self._unprocessed_value])
        else:
            return self._unprocessed_value
