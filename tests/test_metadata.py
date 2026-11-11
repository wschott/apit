import pytest

from apit.core.metadata.album import Album
from apit.core.metadata.media_kind import MediaKind
from apit.core.metadata.rating import Rating
from apit.core.metadata.disc_number import DiscNumber
from apit.core.metadata.track_number import TrackNumber
from apit.core.metadata.song import Song
from apit.core.track_matching import find_song
from apit.core.metadata.song import generate_padded_track_number

from tests.conftest import dummy_song


def test_album():
    album = Album(
        album_artist="Album Artist",
        copyright="℗ 2010 Album Copyright",
        artwork_url="https://cover.url/img/100x100bb.jpg",
    )
    assert album.album_artist == "Album Artist"
    assert album.copyright == "℗ 2010 Album Copyright"
    assert album.artwork_url == "https://cover.url/img/100x100bb.jpg"


def test_song():
    song = Song(
        album=Album(
            album_artist="Album Artist",
            copyright="℗ 2010 Album Copyright",
            artwork_url="https://cover.url/img/100x100bb.jpg",
        ),
        collection_id=12345,
        artist="Track Artist",
        album_name="Test Album Namè",
        media_kind=MediaKind.SONG,
        disc_number=DiscNumber(2),
        disc_total=3,
        track_number=TrackNumber(3),
        track_total=12,
        title="Track (feat. Other & $Artist) [Bonus Track]",
        genre="Test Genré",
        content_id=98765,
        rating=Rating.EXPLICIT,
        release_date="2010-01-01T07:00:00Z",
        compilation=True,
    )

    assert song.album_artist == "Album Artist"
    assert song.copyright == "℗ 2010 Album Copyright"
    assert song.collection_id == 12345
    assert song.artist == "Track Artist"
    assert song.album_name == "Test Album Namè"
    assert song.media_kind == MediaKind.SONG
    assert song.disc_number == 2
    assert song.disc_total == 3
    assert song.track_number == 3
    assert song.track_total == 12
    assert song.title == "Track (feat. Other & $Artist) [Bonus Track]"
    assert song.genre == "Test Genré"
    assert song.content_id == 98765
    assert song.rating == Rating.EXPLICIT
    assert song.release_date == "2010-01-01T07:00:00Z"
    assert song.compilation
    assert song.track_number_padded == "2-03"


def test_find_song():
    first_song = dummy_song(disc=1, track=2)
    second_song = dummy_song(disc=3, track=4)
    songs = [first_song, second_song]

    assert find_song(songs, disc=DiscNumber(3), track=TrackNumber(4)) == second_song


def test_find_song_not_matching():
    assert find_song([], disc=DiscNumber(3), track=TrackNumber(4)) is None
    assert (
        find_song(
            [dummy_song(disc=3, track=4)],
            disc=DiscNumber(3),
            track=TrackNumber(2),
        )
        is None
    )
    assert (
        find_song(
            [dummy_song(disc=3, track=4)],
            disc=DiscNumber(1),
            track=TrackNumber(4),
        )
        is None
    )


@pytest.mark.parametrize(
    ("track_number", "track_total", "disc_number", "disc_total", "expected"),
    [
        (3, 5, 1, 1, "3"),
        (3, 11, 1, 1, "03"),
        (3, 5, 1, 2, "1-3"),
        (3, 5, 2, 2, "2-3"),
        (3, 11, 2, 2, "2-03"),
        (3, 5, 2, 11, "02-3"),
        (3, 11, 2, 11, "02-03"),
    ],
)
def test_generate_padded_track_number(
    track_number: int,
    track_total: int,
    disc_number: int,
    disc_total: int,
    expected: str,
):
    assert (
        generate_padded_track_number(
            track_number=TrackNumber(track_number),
            track_total=track_total,
            disc_number=DiscNumber(disc_number),
            disc_total=disc_total,
        )
        == expected
    )
