import os
from typing import Any

from apit.commands.show.reporting.readable_names import MEDIA_TYPE_TO_HUMAN_READABLE
from apit.commands.show.reporting.readable_names import MP4_MAPPING_TO_HUMAN_READABLE
from apit.commands.show.reporting.readable_names import RATING_TO_HUMAN_READABLE
from apit.store.constants import MP4_MAPPING


class TagIdDescriptionValue:
    def __init__(self, tag_id: str, value: Any) -> None:
        self.tag_id: str = tag_id
        self._unprocessed_value: Any = value

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.tag_id == other
        return False

    def description(self, verbose: bool) -> str:
        if description := _get_human_readable_description(self.tag_id):
            return f"{description} ({self.tag_id})" if verbose else description
        return self.tag_id

    def value(self, verbose: bool) -> str:
        if self.tag_id in [
            MP4_MAPPING.COMPILATION,
            MP4_MAPPING.GAPLESS,
        ]:  # no list
            return "<yes>" if self._unprocessed_value else "<no>"
        elif self.tag_id == MP4_MAPPING.RATING:  # list
            return RATING_TO_HUMAN_READABLE[int(self._unprocessed_value[0])]
        elif self.tag_id == MP4_MAPPING.MEDIA_TYPE:  # list
            return MEDIA_TYPE_TO_HUMAN_READABLE[self._unprocessed_value[0]]
        elif self.tag_id == MP4_MAPPING.LYRICS:  # list
            lyrics = self._unprocessed_value[0]
            if verbose:
                return lyrics.replace("\r", os.linesep)
            return "<present>"
        elif self.tag_id == MP4_MAPPING.ARTWORK:  # list
            return f"<{len(self._unprocessed_value)} present>"
        elif self.tag_id in [  # list w/ one tuple
            MP4_MAPPING.TRACK_NUMBER,
            MP4_MAPPING.DISC_NUMBER,
        ]:
            item = self._unprocessed_value[0][0] or "<none>"
            total_items = self._unprocessed_value[0][1] or "<none>"
            return f"{item}/{total_items}"
        if isinstance(self._unprocessed_value, list):  # most tags
            return "".join([str(x) for x in self._unprocessed_value])
        else:
            return self._unprocessed_value


def _get_human_readable_description(key: str) -> str | None:
    if new_key := _get_mp4_mapping(key):
        return MP4_MAPPING_TO_HUMAN_READABLE.get(new_key, "")
    return None


def _get_mp4_mapping(key: str) -> MP4_MAPPING | None:
    try:
        return MP4_MAPPING(key)
    except ValueError:
        return None
