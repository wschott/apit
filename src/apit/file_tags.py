from apit.readable_names import ReadableTagName
from apit.tagged_value import TaggedValue


class FileTags:
    def __init__(self, tags: list[TaggedValue]) -> None:
        self._tags: list[TaggedValue] = tags

    @property
    def has_tags(self) -> bool:
        return len(self._tags) > 0

    def filter(self, names_to_select: list[ReadableTagName]) -> list[TaggedValue]:
        name_to_tag_map = {tag.readable_name: tag for tag in self._tags if tag.is_known}
        return [tag for name in names_to_select if (tag := name_to_tag_map.get(name))]

    def filter_unknown(self) -> list[TaggedValue]:
        return [tag for tag in self._tags if not tag.is_known]
