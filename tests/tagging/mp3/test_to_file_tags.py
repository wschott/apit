from unittest.mock import MagicMock

import mutagen.id3
import pytest

from apit.core.audio.tag_name import TagName
from apit.core.audio.tag_value import ArtworkValue
from apit.core.audio.tag_value import FlagValue
from apit.core.audio.tag_value import LyricsValue
from apit.core.audio.tag_value import TextValue
from apit.file_types.mp3.to_file_tags import to_file_tags

APIC = mutagen.id3.APIC(encoding=3, mime="image/jpeg", type=3, desc="", data=b"x")


def _only_tag(tag_id, raw):
    file_tags = to_file_tags(MagicMock(tags={tag_id: raw}))
    [tag] = file_tags.tags
    return tag


@pytest.mark.parametrize(
    ("tag_id", "raw", "name", "value"),
    [
        (
            "USLT::eng",
            mutagen.id3.USLT(encoding=3, lang="eng", desc="", text="a\rb"),
            TagName.LYRICS,
            LyricsValue("a\rb"),
        ),
        ("APIC:", APIC, TagName.ARTWORK, ArtworkValue(None)),
        ("APIC:cover", APIC, None, ArtworkValue(None)),
        (
            "TCMP",
            mutagen.id3.TCMP(encoding=3, text=["1"]),
            TagName.COMPILATION,
            FlagValue(True),
        ),
        (
            "TCMP",
            mutagen.id3.TCMP(encoding=3, text=["0"]),
            TagName.COMPILATION,
            FlagValue(False),
        ),
        (
            "COMM:iTunPGAP:eng",
            mutagen.id3.COMM(encoding=3, lang="eng", desc="iTunPGAP", text=["1"]),
            TagName.GAPLESS,
            FlagValue(True),
        ),
        (
            "TIT2",
            mutagen.id3.TIT2(encoding=3, text=["Hello"]),
            TagName.TITLE,
            TextValue("Hello"),
        ),
        (
            "TRCK",
            mutagen.id3.TRCK(encoding=3, text=["1/2"]),
            TagName.TRACK_NUMBER,
            TextValue("1/2"),
        ),
        (
            "ZZZZ",
            mutagen.id3.TIT2(encoding=3, text=["Other"]),
            None,
            TextValue("Other"),
        ),
    ],
)
def test_to_file_tags(tag_id, raw, name, value):
    tag = _only_tag(tag_id, raw)

    assert tag.tag_id == tag_id
    assert tag.name == name
    assert tag.value == value


def test_no_tags():
    assert not to_file_tags(MagicMock(tags=None)).has_tags
