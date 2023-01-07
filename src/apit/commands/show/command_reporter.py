from collections.abc import Callable
from collections.abc import Iterable
from dataclasses import dataclass

from apit.commands.show.reporting.file_tags import FileTags
from apit.commands.show.reporting.named_tag_sections import ORDER_ALBUM
from apit.commands.show.reporting.named_tag_sections import ORDER_IDS
from apit.commands.show.reporting.named_tag_sections import ORDER_MISC
from apit.commands.show.reporting.named_tag_sections import ORDER_TRACK
from apit.commands.show.reporting.named_tag_sections import ORDER_USER
from apit.commands.show.reporting.readable_names import ReadableTagName
from apit.commands.show.reporting.tag_id_description import TagIdDescriptionValue
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
    values: list[tuple[str, str]]


def print_tags(file_tags: FileTags, verbose: bool) -> str:
    known_sections = to_metadata_sections(file_tags, KNOWN_NAMED_SECTIONS, verbose)
    unknown_sections = [
        MetadataSection(
            "Unknown",
            to_table_rows(
                sorted(
                    file_tags.filter_unknown(),
                    key=lambda tag_id_desc_value: tag_id_desc_value.tag_id,
                ),
                verbose,
            ),
        )
    ]

    max_tag_description_length = calculate_tag_max_len(known_sections)
    metadata_tables: list[str] = [
        metadata_table(
            section.title,
            metadata_inline_table(section.values, max_tag_description_length),
        )
        for section in (known_sections + unknown_sections)
    ]
    return "\n\n".join(metadata_tables)


def to_metadata_sections(
    file_tags: FileTags, sections: Iterable[NamedSection], verbose: bool
) -> list[MetadataSection]:
    return [
        MetadataSection(section.title, section_tag_values)
        for section in sections
        if (
            section_tag_values := to_table_rows(
                file_tags.filter(section.readable_tag_names), verbose
            )
        )
    ]


def to_table_rows(
    tags: Iterable[TagIdDescriptionValue], verbose: bool
) -> list[tuple[str, str]]:
    return [(tag.description(verbose), tag.value(verbose)) for tag in tags]


def calculate_tag_max_len(sections: Iterable[MetadataSection]) -> int:
    extract_values: Callable[
        [MetadataSection], list[tuple[str, str]]
    ] = lambda x: x.values

    values_of_sections: list[tuple[str, str]] = flat_map(extract_values, sections)
    return max(len(description) for description, _ in values_of_sections)
