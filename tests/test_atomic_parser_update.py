from pathlib import Path
from unittest.mock import MagicMock, call

import mutagen
import pytest

from apit.atomic_parser import (
    _modify_mp4_file,
    _read_artwork_content,
    update_metadata,
)
from apit.error import ApitError
from apit.metadata import Song
from apit.store.constants import MP4_MAPPING


def test_modify_mp4_file(test_song: Song):
    mock_mp4_file = {}
    updated_mock_mp4_file = _modify_mp4_file(mock_mp4_file, test_song)

    assert updated_mock_mp4_file[MP4_MAPPING.ARTIST.value] == test_song.artist
    assert updated_mock_mp4_file[MP4_MAPPING.TITLE.value] == test_song.title
    assert updated_mock_mp4_file[MP4_MAPPING.ALBUM_NAME.value] == test_song.album_name
    assert updated_mock_mp4_file[MP4_MAPPING.GENRE.value] == test_song.genre
    assert updated_mock_mp4_file[MP4_MAPPING.RELEASE_DATE.value] == test_song.release_date
    assert updated_mock_mp4_file[MP4_MAPPING.DISC_NUMBER.value] == [(test_song.disc_number, test_song.disc_total)]
    assert updated_mock_mp4_file[MP4_MAPPING.TRACK_NUMBER.value] == [(test_song.track_number, test_song.track_total)]
    assert updated_mock_mp4_file[MP4_MAPPING.RATING.value] == [1]
    assert updated_mock_mp4_file[MP4_MAPPING.MEDIA_TYPE.value] == [1]
    assert updated_mock_mp4_file[MP4_MAPPING.ALBUM_ARTIST.value] == test_song.album_artist
    assert updated_mock_mp4_file[MP4_MAPPING.COPYRIGHT.value] == test_song.copyright
    assert updated_mock_mp4_file[MP4_MAPPING.COMPILATION.value] == test_song.compilation
    assert updated_mock_mp4_file[MP4_MAPPING.CONTENT_ID.value] == [test_song.content_id]
    assert MP4_MAPPING.ARTWORK.value not in updated_mock_mp4_file


def test_modify_mp4_file_with_cover(test_song: Song):
    mock_mp4_file = {}
    updated_mock_mp4_file = _modify_mp4_file(mock_mp4_file, test_song, artwork='artwork-value')

    assert updated_mock_mp4_file[MP4_MAPPING.ARTWORK.value] == ['artwork-value']
    assert updated_mock_mp4_file[MP4_MAPPING.ARTIST.value] == test_song.artist


def test_metadata_updating(monkeypatch, test_song: Song):
    mock_mp4_file = MagicMock()
    monkeypatch.setattr('apit.atomic_parser.read_metadata', lambda *args: mock_mp4_file)

    result = update_metadata(Path('dummy.m4a'), test_song)

    assert mock_mp4_file.save.call_args == call()
    assert result == mock_mp4_file


def test_metadata_updating_with_artwork(monkeypatch, test_song: Song):
    cover_path = 'cover.jpg'
    mock_mp4_file = MagicMock()
    monkeypatch.setattr('apit.atomic_parser.read_metadata', lambda *args: mock_mp4_file)
    mock_read_artwork_content = MagicMock()
    monkeypatch.setattr('apit.atomic_parser._read_artwork_content', mock_read_artwork_content)
    mock_modify_mp4_file = MagicMock()
    monkeypatch.setattr('apit.atomic_parser._modify_mp4_file', mock_modify_mp4_file)

    result = update_metadata(Path('dummy.m4a'), test_song, cover_path)

    assert mock_read_artwork_content.call_args == call(cover_path)
    assert mock_modify_mp4_file.call_args == call(mock_mp4_file, test_song, mock_read_artwork_content())
    assert mock_mp4_file.save.call_args == call()
    assert result == mock_mp4_file


def test_metadata_updating_file_read_error(monkeypatch, test_song):
    def _raise(*args):
        raise ApitError('read-error')
    monkeypatch.setattr('apit.atomic_parser.read_metadata', _raise)

    with pytest.raises(ApitError, match='read-error'):
        update_metadata(Path('dummy.m4a'), test_song)


def test_metadata_updating_file_save_error(monkeypatch, test_song):
    mock_mp4_file = MagicMock()
    mock_mp4_file.save.side_effect = mutagen.MutagenError('save-error')
    monkeypatch.setattr('apit.atomic_parser.read_metadata', lambda *args: mock_mp4_file)

    with pytest.raises(ApitError, match='save-error'):
        update_metadata(Path('dummy.m4a'), test_song)
    assert mock_mp4_file.save.call_args == call()


def test_read_artwork_content_with_jpg(monkeypatch):
    mock_cover_path = MagicMock(suffix='.jpg')
    mock_cover_path.read_bytes.return_value = 'artwork-value'

    mock_mp4_cover = MagicMock(FORMAT_JPEG='jpg')
    monkeypatch.setattr('mutagen.mp4.MP4Cover', mock_mp4_cover)

    artwork = _read_artwork_content(mock_cover_path)

    assert mock_mp4_cover.call_args == call('artwork-value', imageformat='jpg')
    assert artwork == mock_mp4_cover()


def test_read_artwork_content_with_png(monkeypatch):
    mock_cover_path = MagicMock(suffix='.png')
    mock_cover_path.read_bytes.return_value = 'artwork-value'

    mock_mp4_cover = MagicMock(FORMAT_PNG='png')
    monkeypatch.setattr('mutagen.mp4.MP4Cover', mock_mp4_cover)

    artwork = _read_artwork_content(mock_cover_path)

    assert mock_mp4_cover.call_args == call('artwork-value', imageformat='png')
    assert artwork == mock_mp4_cover()


def test_read_artwork_content_with_unsupported_filetype():
    with pytest.raises(ApitError, match='Unknown artwork image type'):
        _read_artwork_content(MagicMock(suffix='.uns'))
