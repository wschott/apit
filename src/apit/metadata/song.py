from dataclasses import dataclass

from apit.metadata import Album
from apit.utils import generate_padded_track_number


@dataclass
class Song:
    album: Album
    track_number: int
    track_total: int
    disc_number: int
    disc_total: int
    title: str
    artist: str
    release_date: str
    genre: str
    album_name: str
    content_id: int
    collection_id: int
    rating: str
    media_kind: str
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
    def artwork_url(self) -> str:
        return self.album.artwork_url

    @property
    def track_number_padded(self) -> str:
        return generate_padded_track_number(
            track_number=self.track_number,
            track_total=self.track_total,
            disc_number=self.disc_number,
            disc_total=self.disc_total,
        )
