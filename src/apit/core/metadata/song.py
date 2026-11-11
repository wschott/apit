from dataclasses import dataclass

from apit.core.metadata.album import Album
from apit.core.metadata.media_kind import MediaKind
from apit.core.metadata.rating import Rating
from apit.core.metadata.disc_number import DiscNumber
from apit.core.metadata.track_number import TrackNumber
from apit.utils.padded_number import padded_number


@dataclass
class Song:
    album: Album
    track_number: TrackNumber
    track_total: int
    disc_number: DiscNumber
    disc_total: int
    title: str
    artist: str
    release_date: str
    genre: str
    album_name: str
    content_id: int
    collection_id: int
    rating: Rating
    media_kind: MediaKind
    compilation: bool

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} '{self.track_number_padded} {self.title}'>"

    def __repr__(self) -> str:
        return str(self)

    @property
    def copyright(self) -> str:
        return self.album.copyright

    @property
    def album_artist(self) -> str:
        return self.album.album_artist

    @property
    def track_number_padded(self) -> str:
        return generate_padded_track_number(
            track_number=self.track_number,
            track_total=self.track_total,
            disc_number=self.disc_number,
            disc_total=self.disc_total,
        )


def generate_padded_track_number(
    track_number: TrackNumber,
    track_total: int,
    disc_number: DiscNumber,
    disc_total: int,
) -> str:
    if disc_total > 1:
        return f"{padded_number(disc_number, disc_total)}-{padded_number(track_number, track_total)}"
    return padded_number(track_number, track_total)
