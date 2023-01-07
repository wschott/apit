from collections.abc import Iterable
from dataclasses import dataclass

from apit.commands.show.reporting.file_tags import FileTags
from apit.commands.show.reporting.named_tag_sections import ORDER_ALBUM
from apit.commands.show.reporting.named_tag_sections import ORDER_IDS
from apit.commands.show.reporting.named_tag_sections import ORDER_MISC
from apit.commands.show.reporting.named_tag_sections import ORDER_TRACK
from apit.commands.show.reporting.named_tag_sections import ORDER_USER
from apit.commands.show.reporting.readable_names import ReadableTagName
from apit.commands.show.reporting.tagged_value import TaggedValue
from apit.list_utils import flat_map
from apit.reporting.table import metadata_inline_table
from apit.reporting.table import metadata_table


@dataclass
class NamedSection:
    title: str
    readable_tag_names: Iterable[ReadableTagName]


KNOWN_NAMED_SECTIONS: list[NamedSection] = [
    NamedSection("Track", ORDER_TRACK),
    NamedSection("Album", ORDER_ALBUM),
    NamedSection("IDs", ORDER_IDS),
    NamedSection("Misc", ORDER_MISC),
    NamedSection("User", ORDER_USER),
]


@dataclass
class MetadataSection:
    title: str
    tags: Iterable[TaggedValue]


def print_tags(file_tags: FileTags, verbose: bool) -> str:
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


def filter_valid_sections(sections: Iterable[MetadataSection]) -> list[MetadataSection]:
    return [section for section in sections if section.tags]


def to_printable_tables(
    sections: Iterable[MetadataSection],
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


def to_table_rows(tags: Iterable[TaggedValue], verbose: bool) -> list[tuple[str, str]]:
    return [(tag.description(verbose), tag.value(verbose)) for tag in tags]


def calculate_tag_max_len(sections: Iterable[MetadataSection], verbose: bool) -> int:
    tags: list[TaggedValue] = flat_map(lambda section: section.tags, sections)
    return max(len(tag.description(verbose)) for tag in tags if tag.is_known)
