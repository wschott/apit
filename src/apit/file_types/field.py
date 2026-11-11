from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from apit.core.audio.tag_id import TagIdEnum
from apit.core.audio.tag_name import TagName
from apit.core.audio.tag_value import TagValue
from apit.core.metadata.artwork import Artwork
from apit.core.metadata.song import Song


type DecodeFn = Callable[[Any], TagValue]
type EncodeFn = Callable[[TagIdEnum, Song, Artwork | None], Any]


@dataclass(frozen=True)
class Field:
    name: TagName
    tag_id: TagIdEnum
    decode: DecodeFn | None = None  # None: the format's default
    encode: EncodeFn | None = None  # None: read-only
