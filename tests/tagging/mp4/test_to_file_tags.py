from unittest.mock import MagicMock

import mutagen.mp4
import pytest

from apit.core.audio.tag_name import TagName
from apit.core.audio.tag_value import ArtworkValue
from apit.core.audio.tag_value import FlagValue
from apit.core.audio.tag_value import LyricsValue
from apit.core.audio.tag_value import MediaKindValue
from apit.core.audio.tag_value import NumberOfTotalValue
from apit.core.audio.tag_value import RatingValue
from apit.core.audio.tag_value import TextValue
from apit.core.metadata.media_kind import MediaKind
from apit.core.metadata.rating import Rating
from apit.file_types.mp4.to_file_tags import to_file_tags


def _only_tag(tag_id, raw):
    file_tags = to_file_tags(MagicMock(tags={tag_id: raw}))
    [tag] = file_tags.tags
    return tag


@pytest.mark.parametrize(
    ("tag_id", "raw", "name", "value"),
    [
        ("cpil", True, TagName.COMPILATION, FlagValue(True)),
        ("pgap", False, TagName.GAPLESS, FlagValue(False)),
        ("rtng", [0], TagName.RATING, RatingValue(Rating.NONE)),
        ("rtng", [1], TagName.RATING, RatingValue(Rating.EXPLICIT)),
        ("rtng", [2], TagName.RATING, RatingValue(Rating.CLEAN)),
        ("stik", [1], TagName.MEDIA_TYPE, MediaKindValue(MediaKind.SONG)),
        ("\xa9lyr", ["a\rb"], TagName.LYRICS, LyricsValue("a\rb")),
        (
            "covr",
            [mutagen.mp4.MP4Cover(b"x"), mutagen.mp4.MP4Cover(b"y")],
            TagName.ARTWORK,
            ArtworkValue(2),
        ),
        ("trkn", [(1, 12)], TagName.TRACK_NUMBER, NumberOfTotalValue(1, 12)),
        ("disk", [(None, None)], TagName.DISC_NUMBER, NumberOfTotalValue(None, None)),
        ("\xa9ART", ["a", "b"], TagName.ARTIST, TextValue("ab")),
        ("tmpo", [120], TagName.BPM, TextValue("120")),
        ("zzzz", "scalar", None, TextValue("scalar")),
        ("zzzz", ["l1", "l2"], None, TextValue("l1l2")),
    ],
)
def test_to_file_tags(tag_id, raw, name, value):
    tag = _only_tag(tag_id, raw)

    assert tag.tag_id == tag_id
    assert tag.name == name
    assert tag.value == value


@pytest.mark.parametrize(
    ("tag_id", "raw", "expected"),
    [("rtng", [9], "9"), ("stik", [9], "9")],
)
def test_unrecognized_enumerated_values_fall_back_to_text(tag_id, raw, expected):
    assert _only_tag(tag_id, raw).value == TextValue(expected)


def test_no_tags():
    assert not to_file_tags(MagicMock(tags=None)).has_tags
