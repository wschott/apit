from collections.abc import Sequence

from .album import Album  # noqa: F401
from .song import Song


def find_song(
    songs: Sequence[Song], disc: int | None, track: int | None
) -> Song | None:
    for song in songs:
        if song.disc_number == disc and song.track_number == track:
            return song
    return None  # TODO raise?
