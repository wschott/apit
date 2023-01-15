from unittest.mock import MagicMock

from apit.tagging.mp4.update import is_itunes_bought_file


def test_is_itunes_bought_file_for_itunes_file():
    mp4_file = MagicMock(
        tags={
            "apID": "owner information",
            "aART": "Album Artist",
        }
    )
    assert is_itunes_bought_file(mp4_file)

    MagicMock(
        tags={
            "ownr": "owner information",
            "aART": "Album Artist",
        }
    )
    assert is_itunes_bought_file(mp4_file)


def test_is_itunes_bought_file_for_not_itunes_file():
    mp4_file = MagicMock(
        tags={
            "trkn": "owner information",
            "aART": "Album Artist",
        }
    )
    assert not is_itunes_bought_file(mp4_file)


def test_is_itunes_bought_file_error():
    mp4_file = MagicMock(tags={})
    assert not is_itunes_bought_file(mp4_file)
