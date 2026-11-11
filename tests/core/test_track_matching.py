from pathlib import Path

import pytest

from apit.core.track_matching import Match
from apit.core.track_matching import MatchQuality
from apit.core.track_matching import SkipReason
from apit.core.track_matching import extract_disc_number
from apit.core.track_matching import extract_track_number
from apit.core.track_matching import match

from tests.conftest import dummy_song


@pytest.mark.parametrize(
    "path",
    [
        "14.m4a",
        "14..m4a",
        "#14.m4a",
        "14 song title.m4a",
        "14song title.m4a",
        "14. song title.m4a",
        "14.song title.m4a",
        "#14 song title.m4a",
    ],
)
def test_extract_disc_and_track_number_using_only_track_number(path: str):
    assert extract_disc_number(Path(path)) is None
    assert extract_track_number(Path(path)) == 14


@pytest.mark.parametrize(
    "path",
    [
        "2 14 song title.m4a",
        "2. 14 song title.m4a",
        "2. 14. song title.m4a",
    ],
)
def test_extract_disc_and_track_number_using_only_track_number_containing_numbers_in_title(
    path: str,
):
    assert extract_disc_number(Path(path)) is None
    assert extract_track_number(Path(path)) == 2


@pytest.mark.parametrize(
    "path",
    [
        "2-14.m4a",
        "2.14.m4a",
        "2.14..m4a",
        "2.14..m4a",
        "#2-14.m4a",
        "2-14song title.m4a",
        "2-14 song title.m4a",
        "2.14 song title.m4a",
        "2.14.song title.m4a",
        "2-14.song title.m4a",
        "2.14. song title.m4a",
        "2-14. song title.m4a",
    ],
)
def test_extract_disc_and_track_number_using_disc_and_track_number(path: str):
    assert extract_disc_number(Path(path)) == 2
    assert extract_track_number(Path(path)) == 14


def test_extract_disc_and_track_number_using_invalid_filename():
    assert extract_disc_number(Path("song title.m4a")) is None
    assert extract_track_number(Path("song title.m4a")) is None


def test_match_exact():
    file = Path("2-3 Track (feat. Other & $Artist) [Bonus Track].m4a")
    song = dummy_song(disc=2, track=3)

    assert match([file], [song]) == [Match(file, song, MatchQuality.EXACT, None)]


def test_match_without_disc_number_assumes_disc_1():
    file = Path("3 Track (feat. Other & $Artist) [Bonus Track].m4a")
    song = dummy_song(disc=1, track=3)

    assert match([file], [song]) == [Match(file, song, MatchQuality.EXACT, None)]


def test_match_without_disc_number_does_not_match_other_disc():
    file = Path("3 song title.m4a")

    result = match([file], [dummy_song(disc=2, track=3)])[0]

    assert result.skip_reason is SkipReason.NO_METADATA


def test_match_exact_ignores_strange_characters_and_case():
    song = dummy_song(disc=2, track=3)
    file = Path("2-3 track! feat.=; [Other & $Artist]_Bonus Track-.m4a")

    assert match([file], [song])[0].quality is MatchQuality.EXACT


def test_match_differs_when_title_differs():
    song = dummy_song(disc=2, track=3)
    file = Path("2-3 any unknown song name.m4a")

    assert match([file], [song]) == [Match(file, song, MatchQuality.DIFFERS, None)]


def test_match_without_track_number():
    file = Path("song title.m4a")

    result = match([file], [dummy_song()])[0]

    assert result == Match(file, None, MatchQuality.NONE, SkipReason.NO_TRACK_NUMBER)
    assert not result.actionable


def test_match_without_metadata():
    file = Path("1 song title.m4a")

    result = match([file], [])[0]

    assert result == Match(file, None, MatchQuality.NONE, SkipReason.NO_METADATA)
    assert not result.actionable


def test_match_with_other_disc_has_no_metadata():
    file = Path("1-3 song title.m4a")

    result = match([file], [dummy_song(disc=2, track=3)])[0]

    assert result.skip_reason is SkipReason.NO_METADATA


def test_match_multiple_files_keeps_order():
    first = dummy_song(disc=1, track=1)
    second = dummy_song(disc=1, track=2)
    files = [Path("2 b.m4a"), Path("x.m4a"), Path("1 a.m4a")]

    result = match(files, [first, second])

    assert [m.file for m in result] == files
    assert [m.song for m in result] == [second, None, first]
