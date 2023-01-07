from collections.abc import Iterable

from apit.commands.show.reporting.readable_names import ReadableTagName
from apit.commands.show.reporting.tag_id_description import TagIdDescriptionValue


class FileTags:
    def __init__(self, all_tag_values: Iterable[TagIdDescriptionValue]) -> None:
        self._all_tag_values: Iterable[TagIdDescriptionValue] = all_tag_values

    def filter(
        self, names_to_select: Iterable[ReadableTagName]
    ) -> list[TagIdDescriptionValue]:
        name_to_tag_map = {tag.readable_name: tag for tag in self._all_tag_values}
        return [
            tag for name in names_to_select if (tag := name_to_tag_map.get(name, None))
        ]

    def filter_unknown(self) -> list[TagIdDescriptionValue]:
        return [
            tagged_value
            for tagged_value in self._all_tag_values
            if not tagged_value.readable_name
        ]
