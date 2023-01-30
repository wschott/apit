from pathlib import Path
from unittest.mock import MagicMock

import mutagen.mp4
import pytest

from apit.errors import ApitError
from apit.file_types.mp4.read import read_metadata_raw


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

    result = read_metadata_raw(Path("dummy.m4a"))

    assert result.tags["trkn"] == "1/2"
    assert result.tags["aART"] == "Album Artist"


def test_metadata_reading_error(monkeypatch):
    def _raise(*args):
        raise mutagen.mp4.MP4StreamInfoError("mock-error")

    monkeypatch.setattr("mutagen.mp4.MP4", _raise)

    with pytest.raises(ApitError, match="mock-error"):
        read_metadata_raw(Path("dummy.m4a"))
