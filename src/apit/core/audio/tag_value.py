from dataclasses import dataclass

from apit.core.metadata.media_kind import MediaKind
from apit.core.metadata.rating import Rating


@dataclass(frozen=True)
class TextValue:
    text: str


@dataclass(frozen=True)
class FlagValue:
    enabled: bool


@dataclass(frozen=True)
class RatingValue:
    rating: Rating


@dataclass(frozen=True)
class MediaKindValue:
    kind: MediaKind


@dataclass(frozen=True)
class NumberOfTotalValue:
    number: int | None
    total: int | None


@dataclass(frozen=True)
class LyricsValue:
    text: str


@dataclass(frozen=True)
class ArtworkValue:
    count: int | None  # None: the format does not tell how many


type TagValue = (
    TextValue
    | FlagValue
    | RatingValue
    | MediaKindValue
    | NumberOfTotalValue
    | LyricsValue
    | ArtworkValue
)
