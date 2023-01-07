from collections.abc import Iterable

from apit.commands.show.reporting.readable_names import ReadableTagName
from apit.commands.show.reporting.tagged_value import TaggedValue


class FileTags:
    def __init__(self, tags: Iterable[TaggedValue]) -> None:
        self._tags: Iterable[TaggedValue] = tags

    def filter(self, names_to_select: Iterable[ReadableTagName]) -> list[TaggedValue]:
        name_to_tag_map = {tag.readable_name: tag for tag in self._tags if tag.is_known}
        return [
            tag for name in names_to_select if (tag := name_to_tag_map.get(name, None))
        ]

    def filter_unknown(self) -> list[TaggedValue]:
        return [tag for tag in self._tags if not tag.is_known]
