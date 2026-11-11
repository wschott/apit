import os

import pytest

from apit.core.audio.tag_id import TagId
from apit.core.audio.tag_name import TagName
from apit.core.audio.tag_value import ArtworkValue
from apit.core.audio.tag_value import FlagValue
from apit.core.audio.tag_value import LyricsValue
from apit.core.audio.tag_value import MediaKindValue
from apit.core.audio.tag_value import NumberOfTotalValue
from apit.core.audio.tag_value import RatingValue
from apit.core.audio.tag_value import TextValue
from apit.core.audio.tagged_value import TaggedValue
from apit.core.metadata.media_kind import MediaKind
from apit.core.metadata.rating import Rating
from apit.infra.cli.tag_text import tag_label
from apit.infra.cli.tag_text import tag_value_text


@pytest.mark.parametrize(
    ("name", "verbose", "expected"),
    [
        (TagName.COMPILATION, False, "Compilation?"),
        (TagName.COMPILATION, True, "Compilation? (cpil)"),
        (None, False, "cpil"),
        (None, True, "cpil"),
    ],
)
def test_tag_label(name, verbose, expected):
    tag = TaggedValue(TagId("cpil"), name, FlagValue(True))

    assert tag_label(tag, verbose) == expected


@pytest.mark.parametrize(
    ("value", "verbose", "expected"),
    [
        (TextValue("Title"), False, "Title"),
        (FlagValue(True), False, "<yes>"),
        (FlagValue(False), True, "<no>"),
        (RatingValue(Rating.NONE), False, "<inoffensive>"),
        (RatingValue(Rating.EXPLICIT), False, "<explicit>"),
        (RatingValue(Rating.CLEAN), False, "<clean>"),
        (MediaKindValue(MediaKind.SONG), False, "<normal>"),
        (NumberOfTotalValue(1, 12), False, "1/12"),
        (NumberOfTotalValue(0, None), False, "<none>/<none>"),
        (NumberOfTotalValue(3, 0), True, "3/<none>"),
        (LyricsValue("a\rb"), False, "<present>"),
        (LyricsValue("a\rb"), True, f"a{os.linesep}b"),
        (ArtworkValue(2), False, "<2 present>"),
        (ArtworkValue(2), True, "<2 present>"),
        (ArtworkValue(None), False, "<present>"),
    ],
)
def test_tag_value_text(value, verbose, expected):
    assert tag_value_text(value, verbose) == expected
