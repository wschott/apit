from collections.abc import Iterable

from apit.commands.show.reporting.tag_id_description import TagIdDescriptionValue
from apit.error import ApitError
from apit.tag_id import TagId


class FileTags:
    def __init__(self, all_tag_values: Iterable[TagIdDescriptionValue]) -> None:
        self._all_tag_values: Iterable[TagIdDescriptionValue] = all_tag_values

    def filter(self, tags_to_select: Iterable[TagId]) -> list[TagIdDescriptionValue]:
        selectable_tags = self._calculate_selectable_tags(tags_to_select)
        return [self._find_tag_value_by(tag_id) for tag_id in selectable_tags]

    def _calculate_selectable_tags(
        self, tags_to_select: Iterable[TagId]
    ) -> list[TagId]:
        tags_in_file = [tag_value.tag_id for tag_value in self._all_tag_values]
        ordered_intersection = [
            tag_id for tag_id in tags_to_select if tag_id in tags_in_file
        ]
        return ordered_intersection

    def _find_tag_value_by(self, tag_id: TagId) -> TagIdDescriptionValue:
        for tag_value in self._all_tag_values:
            if tag_value == tag_id:
                return tag_value
        raise ApitError()

    def get_unknown_tag_ids(self, known_tag_ids: Iterable[TagId]) -> set[TagId]:
        all_tag_ids = {tag_desc_value.tag_id for tag_desc_value in self._all_tag_values}
        return all_tag_ids - set(known_tag_ids)
