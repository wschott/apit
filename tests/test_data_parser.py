import pytest

from apit.error import ApitError
from apit.store_data_parser import extract_album_with_songs


def test_extract_album_with_songs(test_metadata):
    album = extract_album_with_songs(test_metadata)

    assert album['collectionId'] == 1440742903
    assert album['artistName'] == 'Kanye West'
    assert album['collectionName'] == 'My Beautiful Dark Twisted Fantasy'

    song = album.get_song(disc=1, track=3)
    assert song['kind'] == 'song'
    assert song['discNumber'] == 1
    assert song['trackNumber'] == 3
    assert song['trackName'] == 'Power'


def test_extract_album_with_songs_invalid_json():
    with pytest.raises(ApitError):
        extract_album_with_songs('')
    with pytest.raises(ApitError):
        extract_album_with_songs('{"test":[], "resultCount": 0}')
    with pytest.raises(ApitError):
        extract_album_with_songs('{"results":[], "test": 0}')
    with pytest.raises(ApitError):
        extract_album_with_songs('{"results":[], "resultCount": 0}')
