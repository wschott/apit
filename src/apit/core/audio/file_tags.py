from collections.abc import Iterable

from apit.core.audio.tagged_value import TaggedValue


class FileTags:
    def __init__(self, tags: Iterable[TaggedValue]) -> None:
        self._tags: tuple[TaggedValue, ...] = tuple(tags)

    @property
    def tags(self) -> tuple[TaggedValue, ...]:
        return self._tags

    @property
    def has_tags(self) -> bool:
        return len(self._tags) > 0
