from typing import Optional

from .album import Album  # noqa: F401
from .song import Song


def find_song(songs, disc, track) -> Optional[Song]:
    for song in songs:
        if song.disc_number == disc and song.track_number == track:
            return song
    return None  # TODO raise?
