from typing import Any

import mutagen.mp3

from .fields import decode_default
from .fields import MP3_FIELDS_BY_ID
from apit.core.audio.file_tags import FileTags
from apit.core.audio.tag_id import TagId
from apit.core.audio.tagged_value import TaggedValue


def to_file_tags(metadata_file: mutagen.mp3.MP3) -> FileTags:
    if not metadata_file.tags:
        return FileTags([])

    return FileTags(
        [_to_tagged_value(TagId(tag), raw) for tag, raw in metadata_file.tags.items()]
    )


def _to_tagged_value(tag_id: TagId, raw: Any) -> TaggedValue:
    field = MP3_FIELDS_BY_ID.get(tag_id)
    if field is None:
        return TaggedValue(tag_id, None, decode_default(raw))
    decode = field.decode or decode_default
    return TaggedValue(tag_id, field.name, decode(raw))
