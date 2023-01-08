import pytest

from apit.error import ApitError
from apit.metadata import find_song
from apit.store.constants import STORE_KEY
from apit.store.data_parser import _find_album
from apit.store.data_parser import _find_songs
from apit.store.data_parser import extract_by_key
from apit.store.data_parser import extract_songs
from apit.store.data_parser import to_album
from apit.store.data_parser import to_song
from tests.conftest import assert_dummy_test_album
from tests.conftest import assert_dummy_test_song
from tests.conftest import dummy_album


def test_extract_songs(test_metadata):
    songs = extract_songs(test_metadata)

    assert len(songs) == 14

    song = find_song(songs, disc=1, track=3)

    assert song.album_artist == "Kanye West"
    assert song.copyright == "℗ 2010 Roc-A-Fella Records, LLC"

    assert song.collection_id == 1440742903
    assert song.album_name == "My Beautiful Dark Twisted Fantasy"
    assert song.media_kind == "song"
    assert song.disc_number == 1
    assert song.track_number == 3
    assert song.title == "Power"


def test_extract_songs_using_invalid_metadata():
    with pytest.raises(ApitError, match="format error"):
        extract_songs("")
    with pytest.raises(ApitError, match="results empty"):
        extract_songs('{"test":[], "resultCount": 0}')
    with pytest.raises(ApitError, match="results empty"):
        extract_songs('{"results":[], "test": 0}')
    with pytest.raises(ApitError, match="results empty"):
        extract_songs('{"results":[], "resultCount": 0}')


def test_find_album(album_metadata_as_json_obj):
    album = _find_album(album_metadata_as_json_obj)

    assert_dummy_test_album(album)


def test_find_album_using_invalid_metadata():
    with pytest.raises(ApitError, match="No album found"):
        _find_album([])
    with pytest.raises(ApitError, match="No album found"):
        _find_album([{"collectionType": "Not Album"}])


def test_to_album(album_metadata_as_json_obj):
    album = to_album(album_metadata_as_json_obj[0])

    assert_dummy_test_album(album)


def test_to_album_using_invalid_metadata():
    with pytest.raises(ApitError):
        to_album({"invalid-key": "value"})


def test_find_songs(song_metadata_as_json_obj, test_album):
    songs = _find_songs(song_metadata_as_json_obj, test_album)

    assert len(songs) == 2

    song = find_song(songs, disc=2, track=3)
    assert_dummy_test_song(song)


def test_find_songs_using_invalid_metadata():
    test_album = dummy_album()

    assert _find_songs([], test_album) == []
    assert _find_songs([{"something": "not song"}], test_album) == []
    assert _find_songs([{"kind": "not song"}], test_album) == []


def test_to_song(song_metadata_as_json_obj, test_album):
    song = to_song(test_album, song_metadata_as_json_obj[0])

    assert_dummy_test_song(song)


def test_to_song_using_invalid_metadata(test_album):
    with pytest.raises(ApitError):
        to_song(test_album, {"invalid-key": "value"})


def test_extract_by_key():
    assert extract_by_key(STORE_KEY.MEDIA_KIND, {"kind": "song"}) == "song"


def test_extract_by_key_using_invalid_metadata():
    with pytest.raises(ApitError, match="Unknown metadata key"):
        extract_by_key("invalid-key", {"kind": "song"})
    with pytest.raises(ApitError, match="Metadata key not found"):
        extract_by_key(STORE_KEY.MEDIA_KIND, {"invalid-key": "song"})
