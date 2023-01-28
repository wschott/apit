from .album import Album  # noqa: F401
from .artwork import Artwork  # noqa: F401
from .song import Song
from apit.types import DiscNumber
from apit.types import TrackNumber


def find_song(
    songs: list[Song], disc: DiscNumber | None, track: TrackNumber | None
) -> Song | None:
    for song in songs:
        if song.disc_number == disc and song.track_number == track:
            return song
    return None  # TODO raise?
