from dataclasses import dataclass
from typing import Final

from .named_tag_sections import ORDER_ALBUM
from .named_tag_sections import ORDER_IDS
from .named_tag_sections import ORDER_MISC
from .named_tag_sections import ORDER_TRACK
from .named_tag_sections import ORDER_USER
from apit.file_tags import FileTags
from apit.list_utils import flatten
from apit.readable_names import ReadableTagName
from apit.reporting.table import metadata_inline_table
from apit.reporting.table import metadata_table
from apit.tagged_value import TaggedValue


@dataclass
class NamedSection:
    title: str
    readable_tag_names: list[ReadableTagName]


KNOWN_NAMED_SECTIONS: Final[list[NamedSection]] = [
    NamedSection("Track", ORDER_TRACK),
    NamedSection("Album", ORDER_ALBUM),
    NamedSection("IDs", ORDER_IDS),
    NamedSection("Misc", ORDER_MISC),
    NamedSection("User", ORDER_USER),
]


@dataclass
class MetadataSection:
    title: str
    tags: list[TaggedValue]


def to_tags_report(file_tags: FileTags, verbose: bool) -> str:
    known_sections: list[MetadataSection] = [
        MetadataSection(section.title, file_tags.filter(section.readable_tag_names))
        for section in KNOWN_NAMED_SECTIONS
    ]
    unknown_sections = [
        MetadataSection(
            "Unknown", sorted(file_tags.filter_unknown(), key=lambda tag: tag.tag_id)
        )
    ]
    return to_printable_tables(
        filter_valid_sections(known_sections + unknown_sections), verbose
    )


def filter_valid_sections(sections: list[MetadataSection]) -> list[MetadataSection]:
    return [section for section in sections if section.tags]


def to_printable_tables(
    sections: list[MetadataSection],
    verbose: bool,
) -> str:
    max_tag_description_length = calculate_tag_max_len(sections, verbose)
    metadata_tables: list[str] = [
        metadata_table(
            section.title,
            metadata_inline_table(
                to_table_rows(section.tags, verbose), max_tag_description_length
            ),
        )
        for section in sections
    ]
    return "\n\n".join(metadata_tables)


def to_table_rows(tags: list[TaggedValue], verbose: bool) -> list[tuple[str, str]]:
    return [(tag.description(verbose), tag.value(verbose)) for tag in tags]


def calculate_tag_max_len(sections: list[MetadataSection], verbose: bool) -> int:
    tags: list[TaggedValue] = flatten(section.tags for section in sections)
    return max(len(tag.description(verbose)) for tag in tags if tag.is_known)
