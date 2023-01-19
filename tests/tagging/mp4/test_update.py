from pathlib import Path
from unittest.mock import call
from unittest.mock import MagicMock

import mutagen
import pytest

from apit.error import ApitError
from apit.metadata import Artwork
from apit.metadata import Song
from apit.mime_type import MIME_TYPE
from apit.tagging.mp4.constants import MP4_MAPPING
from apit.tagging.mp4.update import _modify_mp4_file
from apit.tagging.mp4.update import _to_artwork
from apit.tagging.mp4.update import update_metadata


def test_modify_mp4_file(test_song: Song):
    mock_mp4_file = _mocked_mp4_file()
    updated_mock_mp4_file = _modify_mp4_file(mock_mp4_file, test_song)

    assert updated_mock_mp4_file[MP4_MAPPING.ARTIST] == test_song.artist
    assert updated_mock_mp4_file[MP4_MAPPING.TITLE] == test_song.title
    assert updated_mock_mp4_file[MP4_MAPPING.ALBUM_NAME] == test_song.album_name
    assert updated_mock_mp4_file[MP4_MAPPING.GENRE] == test_song.genre
    assert updated_mock_mp4_file[MP4_MAPPING.RELEASE_DATE] == test_song.release_date
    assert updated_mock_mp4_file[MP4_MAPPING.DISC_NUMBER] == [
        (test_song.disc_number, test_song.disc_total)
    ]
    assert updated_mock_mp4_file[MP4_MAPPING.TRACK_NUMBER] == [
        (test_song.track_number, test_song.track_total)
    ]
    assert updated_mock_mp4_file[MP4_MAPPING.RATING] == [1]
    assert updated_mock_mp4_file[MP4_MAPPING.MEDIA_TYPE] == [1]
    assert updated_mock_mp4_file[MP4_MAPPING.ALBUM_ARTIST] == test_song.album_artist
    assert updated_mock_mp4_file[MP4_MAPPING.COPYRIGHT] == test_song.copyright
    assert updated_mock_mp4_file[MP4_MAPPING.COMPILATION] == test_song.compilation
    assert updated_mock_mp4_file[MP4_MAPPING.CONTENT_ID] == [test_song.content_id]
    assert MP4_MAPPING.ARTWORK not in updated_mock_mp4_file


def test_modify_mp4_file_with_cover(test_song: Song):
    artwork = Artwork(b"artwork-value", MIME_TYPE.JPEG)
    mock_mp4_file = _mocked_mp4_file()
    updated_mock_mp4_file = _modify_mp4_file(mock_mp4_file, test_song, artwork)

    assert updated_mock_mp4_file[MP4_MAPPING.ARTWORK] == [
        mutagen.mp4.MP4Cover(
            artwork.content, imageformat=mutagen.mp4.MP4Cover.FORMAT_JPEG
        )
    ]
    assert updated_mock_mp4_file[MP4_MAPPING.ARTIST] == test_song.artist


def test_metadata_updating(monkeypatch, test_song: Song):
    mock_mp4_file = MagicMock()
    monkeypatch.setattr(
        "apit.tagging.mp4.update.read_metadata_raw", lambda *args: mock_mp4_file
    )

    result = update_metadata(Path("dummy.m4a"), test_song)

    assert mock_mp4_file.save.call_args == call()
    assert result == mock_mp4_file


def test_metadata_updating_with_artwork(monkeypatch, test_song: Song):
    artwork = Artwork(b"artwork-value", MIME_TYPE.JPEG)
    mock_mp4_file = MagicMock()
    monkeypatch.setattr(
        "apit.tagging.mp4.update.read_metadata_raw", lambda *args: mock_mp4_file
    )
    mock_modify_mp4_file = MagicMock()
    monkeypatch.setattr(
        "apit.tagging.mp4.update._modify_mp4_file", mock_modify_mp4_file
    )

    result = update_metadata(Path("dummy.m4a"), test_song, artwork)

    assert mock_modify_mp4_file.call_args == call(mock_mp4_file, test_song, artwork)
    assert mock_mp4_file.save.call_args == call()
    assert result == mock_mp4_file


def test_metadata_updating_file_read_error(monkeypatch, test_song):
    def _raise(*args):
        raise ApitError("read-error")

    monkeypatch.setattr("apit.tagging.mp4.update.read_metadata_raw", _raise)

    with pytest.raises(ApitError, match="read-error"):
        update_metadata(Path("dummy.m4a"), test_song)


def test_metadata_updating_file_save_error(monkeypatch, test_song):
    mock_mp4_file = MagicMock()
    mock_mp4_file.save.side_effect = mutagen.MutagenError("save-error")
    monkeypatch.setattr(
        "apit.tagging.mp4.update.read_metadata_raw", lambda *args: mock_mp4_file
    )

    with pytest.raises(ApitError, match="save-error"):
        update_metadata(Path("dummy.m4a"), test_song)
    assert mock_mp4_file.save.call_args == call()


def test_to_artwork_with_jpg():
    artwork = Artwork(b"artwork-value", MIME_TYPE.JPEG)

    mp4_artwork = _to_artwork(artwork)

    assert mp4_artwork == mutagen.mp4.MP4Cover(
        b"artwork-value", imageformat=mutagen.mp4.MP4Cover.FORMAT_JPEG
    )


def test_to_artwork_with_png():
    artwork = Artwork(b"artwork-value", MIME_TYPE.PNG)

    mp4_artwork = _to_artwork(artwork)

    assert mp4_artwork == mutagen.mp4.MP4Cover(
        b"artwork-value", imageformat=mutagen.mp4.MP4Cover.FORMAT_PNG
    )


def test_to_artwork_with_unsupported_filetype():
    artwork = Artwork(content=b"artwork-value", mimetype="unknown")

    with pytest.raises(ApitError, match="Unknown artwork mime type"):
        _to_artwork(artwork)


def test_update_fails_for_original_file(monkeypatch, test_song: Song):
    mock_mp4_file = MagicMock(tags={"apID": "owner information"})
    monkeypatch.setattr(
        "apit.tagging.mp4.update.read_metadata_raw", lambda *args: mock_mp4_file
    )

    with pytest.raises(ApitError, match="original iTunes Store file"):
        update_metadata(Path("dummy.m4a"), test_song)


def _mocked_mp4_file() -> MagicMock:
    mocked_dict = MagicMock()
    real_dict: dict = {}
    mocked_dict.__setitem__.side_effect = real_dict.__setitem__
    mocked_dict.__getitem__.side_effect = real_dict.__getitem__
    return mocked_dict
