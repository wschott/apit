from typing import Final

from apit.file_tags import FileTags
from apit.readable_names import ReadableTagName
from apit.reporting.table import metadata_table
from apit.tagged_value import TaggedValue


def to_tags_report(file_tags: FileTags, verbose: bool) -> str:
    known_tags = file_tags.filter(ORDERED_TAGS)
    unknown_tags = sorted(file_tags.filter_unknown(), key=lambda tag: tag.tag_id)

    tags_report: list[str] = []
    if known_tags:
        tags_report.append(_to_tags_report_table(known_tags, verbose))
    if unknown_tags:
        tags_report.append("Unknown Tags")
        tags_report.append(_to_tags_report_table(unknown_tags, verbose))
    return "\n\n".join(tags_report)


def _to_tags_report_table(tags: list[TaggedValue], verbose: bool) -> str:
    max_tag_description_length = _calculate_tag_max_len(tags, verbose)
    return metadata_table(_to_table_rows(tags, verbose), max_tag_description_length)


def _to_table_rows(tags: list[TaggedValue], verbose: bool) -> list[tuple[str, str]]:
    return [(tag.description(verbose), tag.value(verbose)) for tag in tags]


def _calculate_tag_max_len(tags: list[TaggedValue], verbose: bool) -> int:
    return max(len(tag.description(verbose)) for tag in tags)


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
