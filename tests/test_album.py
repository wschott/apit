import pytest

from apit.error import ApitError
from apit.metadata import Song


def test_album(test_album):
    assert test_album['collectionId'] == 12345
    assert test_album['artistName'] == 'Test Artist'
    assert test_album['collectionName'] == 'Test Collection'

def test_album_has_disc(test_album, test_song):
    assert not test_album.has_disc(1)
    assert not test_album.has_disc(2)

    test_album.add_song(test_song)

    assert not test_album.has_disc(1)
    assert test_album.has_disc(2)

def test_album_has_song(test_album, test_song):
    assert not test_album.has_song(1, 1)
    assert not test_album.has_song(2, 3)

    test_album.add_song(test_song)

    assert not test_album.has_song(1, 1)
    assert test_album.has_song(2, 3)

def test_album_add_duplicate_song(test_album, test_song):
    test_album.add_song(test_song)

    with pytest.raises(ApitError):
        test_album.add_song(test_song)

def test_album_get_song_existing(test_album, test_song):
    test_album.add_song(test_song)

    assert test_album.get_song(2, 3) == test_song

def test_album_get_song_non_existing(test_album, test_song):
    with pytest.raises(ApitError):
        test_album.get_song(1, 1)

def test_album_add_songs(test_album, test_song):
    another_test_song = Song({
        'discNumber': 4,
        'trackNumber': 5,
    })
    test_album.add_songs([test_song, another_test_song])

    assert test_album.get_song(2, 3) == test_song
    assert test_album.get_song(4, 5) == another_test_song
