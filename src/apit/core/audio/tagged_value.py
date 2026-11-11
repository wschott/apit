from dataclasses import dataclass

from apit.core.audio.tag_id import TagId
from apit.core.audio.tag_name import TagName
from apit.core.audio.tag_value import TagValue


@dataclass(frozen=True)
class TaggedValue:
    tag_id: TagId
    name: TagName | None
    value: TagValue
