from pathlib import Path
from unittest.mock import MagicMock

import mutagen.mp4
import pytest

from apit.atomic_parser import is_itunes_bought_file
from apit.atomic_parser import read_metadata
from apit.error import ApitError


def test_is_itunes_bought_file_for_itunes_file(monkeypatch):
    monkeypatch.setattr(
        "mutagen.mp4.MP4",
        lambda *args: MagicMock(
            tags={
                "apID": "owner information",
                "aART": "Album Artist",
            }
        ),
    )
    assert is_itunes_bought_file(Path("tests/fixtures/1 itunes file.m4a"))

    monkeypatch.setattr(
        "mutagen.mp4.MP4",
        lambda *args: MagicMock(
            tags={
                "ownr": "owner information",
                "aART": "Album Artist",
            }
        ),
    )
    assert is_itunes_bought_file(Path("tests/fixtures/1 itunes file.m4a"))


def test_is_itunes_bought_file_for_not_itunes_file(monkeypatch):
    monkeypatch.setattr(
        "mutagen.mp4.MP4",
        lambda *args: MagicMock(
            tags={
                "trkn": "owner information",
                "aART": "Album Artist",
            }
        ),
    )
    assert not is_itunes_bought_file(Path("tests/fixtures/1 itunes file.m4a"))


def test_is_itunes_bought_file_error(monkeypatch):
    def _raise(*args):
        raise ApitError

    monkeypatch.setattr("apit.atomic_parser.read_metadata", _raise)
    assert not is_itunes_bought_file(Path("tests/fixtures/1 itunes file.m4a"))


def test_metadata_reading(monkeypatch):
    monkeypatch.setattr(
        "mutagen.mp4.MP4",
        lambda *args: MagicMock(
            tags={
                "trkn": "1/2",
                "aART": "Album Artist",
            }
        ),
    )

    result = read_metadata(Path("dummy.m4a"))

    assert result.tags["trkn"] == "1/2"
    assert result.tags["aART"] == "Album Artist"


def test_metadata_reading_error(monkeypatch):
    def _raise(*args):
        raise mutagen.mp4.MP4StreamInfoError("mock-error")

    monkeypatch.setattr("mutagen.mp4.MP4", _raise)

    with pytest.raises(ApitError, match="mock-error"):
        read_metadata(Path("dummy.m4a"))
