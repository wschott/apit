from typing import Final

from rich.table import Table

from apit.file_tags import FileTags
from apit.readable_names import ReadableTagName
from apit.reporting.table import metadata_table
from apit.tagged_value import TaggedValue


def to_tags_report(file_tags: FileTags, verbose: bool) -> Table:
    known_tags = file_tags.filter(ORDERED_TAGS)
    unknown_tags = sorted(file_tags.filter_unknown(), key=lambda tag: tag.tag_id)

    known_tags_rows = _to_table_rows(known_tags, verbose)
    unknown_tags_rows = _to_table_rows(unknown_tags, verbose)

    return metadata_table(known_tags_rows, unknown_tags_rows)


def _to_table_rows(tags: list[TaggedValue], verbose: bool) -> list[tuple[str, str]]:
    return [(tag.description(verbose), tag.value(verbose)) for tag in tags]


ORDERED_TAGS: Final = [
    ReadableTagName.TITLE,
    ReadableTagName.SORT_ORDER_TITLE,
    ReadableTagName.ARTIST,
    ReadableTagName.SORT_ORDER_ARTIST,
    ReadableTagName.COMPOSER,
    ReadableTagName.SORT_ORDER_COMPOSER,
    ReadableTagName.TRACK_NUMBER,
    ReadableTagName.RATING,
    ReadableTagName.GAPLESS,
    ReadableTagName.BPM,
    ReadableTagName.MEDIA_TYPE,
    ReadableTagName.ALBUM_NAME,
    ReadableTagName.SORT_ORDER_ALBUM,
    ReadableTagName.ALBUM_ARTIST,
    ReadableTagName.SORT_ORDER_ALBUM_ARTIST,
    ReadableTagName.DISC_NUMBER,
    ReadableTagName.COMPILATION,
    ReadableTagName.GENRE,
    ReadableTagName.RELEASE_DATE,
    ReadableTagName.COPYRIGHT,
    ReadableTagName.CONTENT_ID,
    ReadableTagName.PLAYLIST_ID,
    ReadableTagName.ARTIST_ID,
    ReadableTagName.GENRE_ID,
    ReadableTagName.COMPOSER_ID,
    ReadableTagName.ISRC_ID,
    ReadableTagName.TOOL,
    ReadableTagName.GROUPING,
    ReadableTagName.COMMENT,
    ReadableTagName.ARTWORK,
    ReadableTagName.LYRICS,
    ReadableTagName.OWNER_NAME,
    ReadableTagName.USER_MAIL,
    ReadableTagName.PURCHASE_DATE,
    ReadableTagName.STOREFRONT_ID,
]
