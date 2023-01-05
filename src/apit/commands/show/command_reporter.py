from collections.abc import Callable
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from apit.commands.show.reporting.file_tags import FileTags
from apit.commands.show.reporting.tag_id_description import TagIdDescriptionValue
from apit.commands.show.reporting.tag_ordering import ORDERED_ALBUM_TAGS
from apit.commands.show.reporting.tag_ordering import ORDERED_ID_TAGS
from apit.commands.show.reporting.tag_ordering import ORDERED_MISC_TAGS
from apit.commands.show.reporting.tag_ordering import ORDERED_TRACK_TAGS
from apit.commands.show.reporting.tag_ordering import ORDERED_USER_TAGS
from apit.list_utils import flat_map
from apit.reporting.table import metadata_inline_table
from apit.reporting.table import metadata_table


@dataclass
class NamedSection:
    title: str
    tag_ids: Iterable[str]


KNOWN_NAMED_SECTIONS: list[NamedSection] = [
    NamedSection("Track", ORDERED_TRACK_TAGS),
    NamedSection("Album", ORDERED_ALBUM_TAGS),
    NamedSection("IDs", ORDERED_ID_TAGS),
    NamedSection("Misc", ORDERED_MISC_TAGS),
    NamedSection("User", ORDERED_USER_TAGS),
]


@dataclass
class MetadataSection:
    title: str
    values: list[tuple[str, str]]


def print_tags(mp4_tags: Iterable[tuple[str, Any]], verbose: bool) -> str:
    all_tag_value_pairs_in_file: list[TagIdDescriptionValue] = [
        TagIdDescriptionValue(tag_id=tag, value=tag_value)
        for tag, tag_value in mp4_tags
    ]
    file_tags = FileTags(all_tag_value_pairs_in_file)
    known_tag_ids = flat_map(
        lambda known_section: known_section.tag_ids, KNOWN_NAMED_SECTIONS
    )
    unknown_tag_ids = file_tags.get_unknown_tag_ids(known_tag_ids)

    unnamed_sections: list[NamedSection] = [
        NamedSection("Unknown", sorted(unknown_tag_ids))
    ]

    known_sections = to_metadata_sections(file_tags, KNOWN_NAMED_SECTIONS, verbose)
    unknown_sections = to_metadata_sections(file_tags, unnamed_sections, verbose)

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
            section_tag_values := to_named_rows(
                file_tags.filter(section.tag_ids), verbose
            )
        )
    ]


def to_named_rows(
    tags: Iterable[TagIdDescriptionValue], verbose: bool
) -> list[tuple[str, str]]:
    return [(tag.description(verbose), tag.value(verbose)) for tag in tags]


def calculate_tag_max_len(sections: Iterable[MetadataSection]) -> int:
    extract_values: Callable[
        [MetadataSection], list[tuple[str, str]]
    ] = lambda x: x.values

    values_of_sections: list[tuple[str, str]] = flat_map(extract_values, sections)
    return max(len(description) for description, _ in values_of_sections)
