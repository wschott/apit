from typing import NamedTuple

from apit.metadata import Album
from apit.metadata import find_song
from apit.metadata import Song
from apit.types import DiscNumber
from apit.types import TrackNumber


class MockSong(NamedTuple):
    disc_number: int
    track_number: int


def test_album():
    album = Album(
        album_artist="Album Artist",
        copyright="℗ 2010 Album Copyright",
        artwork_url="cover-url",
    )
    assert album.album_artist == "Album Artist"
    assert album.copyright == "℗ 2010 Album Copyright"
    assert album.artwork_url == "cover-url"


def test_song():
    song = Song(
        album=Album(
            album_artist="Album Artist",
            copyright="℗ 2010 Album Copyright",
            artwork_url="cover-url",
        ),
        collection_id=12345,
        artist="Track Artist",
        album_name="Test Album Namè",
        media_kind="song",
        disc_number=DiscNumber(2),
        disc_total=3,
        track_number=TrackNumber(3),
        track_total=12,
        title="Track (feat. Other & $Artist) [Bonus Track]",
        genre="Test Genré",
        content_id=98765,
        rating="explicit",
        release_date="2010-01-01T07:00:00Z",
        compilation=True,
    )

    assert song.album_artist == "Album Artist"
    assert song.copyright == "℗ 2010 Album Copyright"
    assert song.collection_id == 12345
    assert song.artist == "Track Artist"
    assert song.album_name == "Test Album Namè"
    assert song.media_kind == "song"
    assert song.disc_number == 2
    assert song.disc_total == 3
    assert song.track_number == 3
    assert song.track_total == 12
    assert song.title == "Track (feat. Other & $Artist) [Bonus Track]"
    assert song.genre == "Test Genré"
    assert song.content_id == 98765
    assert song.rating == "explicit"
    assert song.release_date == "2010-01-01T07:00:00Z"
    assert song.compilation
    assert song.artwork_url == "cover-url"
    assert song.track_number_padded == "2-03"


def test_find_song():
    first_song = MockSong(disc_number=1, track_number=2)
    second_song = MockSong(disc_number=3, track_number=4)
    songs = [first_song, second_song]

    assert find_song(songs, disc=DiscNumber(3), track=TrackNumber(4)) == second_song


def test_find_song_not_matching():
    assert find_song([], disc=DiscNumber(3), track=TrackNumber(4)) is None
    assert (
        find_song(
            [MockSong(disc_number=DiscNumber(3), track_number=TrackNumber(4))],
            disc=DiscNumber(3),
            track=TrackNumber(2),
        )
        is None
    )
    assert (
        find_song(
            [MockSong(disc_number=DiscNumber(3), track_number=TrackNumber(4))],
            disc=DiscNumber(1),
            track=TrackNumber(4),
        )
        is None
    )
