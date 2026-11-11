import os
from typing import Final

from apit.core.audio.tag_value import ArtworkValue
from apit.core.audio.tag_value import FlagValue
from apit.core.audio.tag_value import LyricsValue
from apit.core.audio.tag_value import MediaKindValue
from apit.core.audio.tag_value import NumberOfTotalValue
from apit.core.audio.tag_value import RatingValue
from apit.core.audio.tag_value import TagValue
from apit.core.audio.tag_value import TextValue
from apit.core.audio.tagged_value import TaggedValue
from apit.core.metadata.media_kind import MediaKind
from apit.core.metadata.rating import Rating
from apit.infra.cli.tag_labels import TAG_LABELS

RATING_TEXT: Final[dict[Rating, str]] = {
    Rating.NONE: "<inoffensive>",
    Rating.EXPLICIT: "<explicit>",
    Rating.CLEAN: "<clean>",
}

MEDIA_KIND_TEXT: Final[dict[MediaKind, str]] = {
    MediaKind.SONG: "<normal>",
    MediaKind.ALBUM: "<album>",
}


def tag_label(tag: TaggedValue, verbose: bool) -> str:
    if tag.name is None:
        return tag.tag_id

    label = TAG_LABELS[tag.name]
    if verbose:
        return f"{label} ({tag.tag_id})"
    return label


def tag_value_text(value: TagValue, verbose: bool) -> str:
    match value:
        case TextValue(text):
            return text
        case FlagValue(enabled):
            return "<yes>" if enabled else "<no>"
        case RatingValue(rating):
            return RATING_TEXT[rating]
        case MediaKindValue(kind):
            return MEDIA_KIND_TEXT[kind]
        case NumberOfTotalValue(number, total):
            return f"{number or '<none>'}/{total or '<none>'}"
        case LyricsValue(text):
            return text.replace("\r", os.linesep) if verbose else "<present>"
        case ArtworkValue(count):
            return "<present>" if count is None else f"<{count} present>"
