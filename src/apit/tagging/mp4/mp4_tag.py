import os

from .constants import Mp4Mapping
from apit.readable_names import ReadableTagName
from apit.store.constants import ITEM_KIND_MAPPING
from apit.store.constants import RATING_MAPPING
from apit.store.constants import StoreKind
from apit.store.constants import StoreRating
from apit.tag_id import TagId
from apit.tagged_value import TaggedValue


class Mp4Tag(TaggedValue):
    def _get_readable_name(self, tag_id: TagId) -> ReadableTagName | None:
        try:
            mapped_tag_id = Mp4Mapping(tag_id)
            return MP4_MAPPING_TO_READABLE_TAG_NAME.get(mapped_tag_id, None)
        except ValueError:
            return None

    def value(self, verbose: bool) -> str:
        if self.tag_id in [
            Mp4Mapping.COMPILATION,
            Mp4Mapping.GAPLESS,
        ]:  # no list
            return "<yes>" if self._unprocessed_value else "<no>"
        elif self.tag_id == Mp4Mapping.RATING:  # list
            return RATING_TO_READABLE_NAME[int(self._unprocessed_value[0])]
        elif self.tag_id == Mp4Mapping.MEDIA_TYPE:  # list
            return MEDIA_TYPE_TO_READABLE_NAME[self._unprocessed_value[0]]
        elif self.tag_id == Mp4Mapping.LYRICS:  # list
            lyrics = self._unprocessed_value[0]
            if verbose:
                return lyrics.replace("\r", os.linesep)
            return "<present>"
        elif self.tag_id == Mp4Mapping.ARTWORK:  # list
            return f"<{len(self._unprocessed_value)} present>"
        elif self.tag_id in [  # list with one tuple
            Mp4Mapping.TRACK_NUMBER,
            Mp4Mapping.DISC_NUMBER,
        ]:
            item = self._unprocessed_value[0][0] or "<none>"
            total_items = self._unprocessed_value[0][1] or "<none>"
            return f"{item}/{total_items}"

        elif isinstance(self._unprocessed_value, list):  # most mp4 tags
            return "".join([str(x) for x in self._unprocessed_value])
        else:
            return self._unprocessed_value


MP4_MAPPING_TO_READABLE_TAG_NAME: dict[Mp4Mapping, ReadableTagName] = {
    Mp4Mapping.TITLE: ReadableTagName.TITLE,
    Mp4Mapping.ARTIST: ReadableTagName.ARTIST,
    Mp4Mapping.ALBUM_NAME: ReadableTagName.ALBUM_NAME,
    Mp4Mapping.ALBUM_ARTIST: ReadableTagName.ALBUM_ARTIST,
    Mp4Mapping.COMPOSER: ReadableTagName.COMPOSER,
    Mp4Mapping.SORT_ORDER_TITLE: ReadableTagName.SORT_ORDER_TITLE,
    Mp4Mapping.SORT_ORDER_ARTIST: ReadableTagName.SORT_ORDER_ARTIST,
    Mp4Mapping.SORT_ORDER_ALBUM: ReadableTagName.SORT_ORDER_ALBUM,
    Mp4Mapping.SORT_ORDER_ALBUM_ARTIST: ReadableTagName.SORT_ORDER_ALBUM_ARTIST,
    Mp4Mapping.SORT_ORDER_COMPOSER: ReadableTagName.SORT_ORDER_COMPOSER,
    Mp4Mapping.TRACK_NUMBER: ReadableTagName.TRACK_NUMBER,
    Mp4Mapping.DISC_NUMBER: ReadableTagName.DISC_NUMBER,
    Mp4Mapping.GENRE: ReadableTagName.GENRE,
    Mp4Mapping.RELEASE_DATE: ReadableTagName.RELEASE_DATE,
    Mp4Mapping.COPYRIGHT: ReadableTagName.COPYRIGHT,
    Mp4Mapping.COMPILATION: ReadableTagName.COMPILATION,
    Mp4Mapping.GAPLESS: ReadableTagName.GAPLESS,
    Mp4Mapping.RATING: ReadableTagName.RATING,
    Mp4Mapping.MEDIA_TYPE: ReadableTagName.MEDIA_TYPE,
    Mp4Mapping.CONTENT_ID: ReadableTagName.CONTENT_ID,
    Mp4Mapping.PLAYLIST_ID: ReadableTagName.PLAYLIST_ID,
    Mp4Mapping.ARTIST_ID: ReadableTagName.ARTIST_ID,
    Mp4Mapping.GENRE_ID: ReadableTagName.GENRE_ID,
    Mp4Mapping.COMPOSER_ID: ReadableTagName.COMPOSER_ID,
    Mp4Mapping.ISRC_ID: ReadableTagName.ISRC_ID,
    Mp4Mapping.GROUPING: ReadableTagName.GROUPING,
    Mp4Mapping.COMMENT: ReadableTagName.COMMENT,
    Mp4Mapping.ARTWORK: ReadableTagName.ARTWORK,
    Mp4Mapping.BPM: ReadableTagName.BPM,
    Mp4Mapping.TOOL: ReadableTagName.TOOL,
    Mp4Mapping.LYRICS: ReadableTagName.LYRICS,
    Mp4Mapping.OWNER_NAME: ReadableTagName.OWNER_NAME,
    Mp4Mapping.USER_MAIL: ReadableTagName.USER_MAIL,
    Mp4Mapping.PURCHASE_DATE: ReadableTagName.PURCHASE_DATE,
    Mp4Mapping.STOREFRONT_ID: ReadableTagName.STOREFRONT_ID,
}


RATING_TO_READABLE_NAME: dict[int, str] = {
    4: "<explicit (old value)>",  # TODO
    RATING_MAPPING[StoreRating.CLEAN]: "<clean>",
    RATING_MAPPING[StoreRating.EXPLICIT]: "<explicit>",
    RATING_MAPPING[StoreRating.NONE]: "<inoffensive>",
}
MEDIA_TYPE_TO_READABLE_NAME: dict[int, str] = {
    ITEM_KIND_MAPPING[StoreKind.SONG]: "<normal>",
}
