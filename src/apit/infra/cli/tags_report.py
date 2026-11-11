from collections.abc import Iterable
from typing import Final

from rich.markup import escape
from rich.table import Table

from apit.core.audio.file_tags import FileTags
from apit.core.audio.tag_name import TagName
from apit.core.audio.tagged_value import TaggedValue
from apit.infra.cli.table import metadata_table
from apit.infra.cli.tag_text import tag_label
from apit.infra.cli.tag_text import tag_value_text


def to_tags_report(file_tags: FileTags, verbose: bool) -> Table:
    known_tags = _filter_known(file_tags.tags, ORDERED_TAGS)
    unknown_tags = sorted(_filter_unknown(file_tags.tags), key=lambda tag: tag.tag_id)

    known_tags_rows = _to_table_rows(known_tags, verbose)
    unknown_tags_rows = _to_table_rows(unknown_tags, verbose)

    return metadata_table(known_tags_rows, unknown_tags_rows)


def _filter_known(
    tags: Iterable[TaggedValue], names_to_select: Iterable[TagName]
) -> list[TaggedValue]:
    name_to_tag_map = {tag.name: tag for tag in tags if not is_tag_known(tag)}
    return [tag for name in names_to_select if (tag := name_to_tag_map.get(name))]


def _filter_unknown(tags: Iterable[TaggedValue]) -> list[TaggedValue]:
    return [tag for tag in tags if is_tag_known(tag)]


def is_tag_known(tag: TaggedValue) -> bool:
    return tag.name is None


def _to_table_rows(tags: Iterable[TaggedValue], verbose: bool) -> list[tuple[str, str]]:
    return [
        (tag_label(tag, verbose), escape(tag_value_text(tag.value, verbose)))
        for tag in tags
    ]


ORDERED_TAGS: Final = [
    TagName.TITLE,
    TagName.SORT_ORDER_TITLE,
    TagName.ARTIST,
    TagName.SORT_ORDER_ARTIST,
    TagName.COMPOSER,
    TagName.SORT_ORDER_COMPOSER,
    TagName.TRACK_NUMBER,
    TagName.RATING,
    TagName.GAPLESS,
    TagName.BPM,
    TagName.MEDIA_TYPE,
    TagName.ALBUM_NAME,
    TagName.SORT_ORDER_ALBUM,
    TagName.ALBUM_ARTIST,
    TagName.SORT_ORDER_ALBUM_ARTIST,
    TagName.DISC_NUMBER,
    TagName.COMPILATION,
    TagName.GENRE,
    TagName.RELEASE_DATE,
    TagName.COPYRIGHT,
    TagName.CONTENT_ID,
    TagName.PLAYLIST_ID,
    TagName.ARTIST_ID,
    TagName.GENRE_ID,
    TagName.COMPOSER_ID,
    TagName.ISRC_ID,
    TagName.TOOL,
    TagName.GROUPING,
    TagName.COMMENT,
    TagName.ARTWORK,
    TagName.LYRICS,
    TagName.OWNER_NAME,
    TagName.USER_MAIL,
    TagName.PURCHASE_DATE,
    TagName.STOREFRONT_ID,
]
