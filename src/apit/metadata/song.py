from apit.metadata import Album


class Song:
    def __init__(self,
                 album: Album,
                 track_number: int,
                 track_total: int,
                 disc_number: int,
                 disc_total: int,
                 title: str,
                 artist: str,
                 release_date: str,
                 genre: str,
                 album_name: str,
                 content_id: int,
                 collection_id: int,
                 rating: str,
                 media_kind: str,
                 compilation: bool,
                 ):
        self._album         = album
        self._track_number  = track_number
        self._track_total   = track_total
        self._disc_number   = disc_number
        self._disc_total    = disc_total
        self._title         = title
        self._artist        = artist
        self._release_date  = release_date
        self._genre         = genre
        self._album_name    = album_name
        self._content_id    = content_id
        self._collection_id = collection_id
        self._rating        = rating
        self._media_kind    = media_kind
        self._compilation   = compilation

    @property
    def copyright(self) -> str:
        return self._album.copyright

    @property
    def album_artist(self) -> str:
        return self._album.album_artist

    @property
    def track_number(self) -> int:
        return self._track_number

    @property
    def track_total(self) -> int:
        return self._track_total

    @property
    def disc_number(self) -> int:
        return self._disc_number

    @property
    def disc_total(self) -> int:
        return self._disc_total

    @property
    def title(self) -> str:
        return self._title

    @property
    def artist(self) -> str:
        return self._artist

    @property
    def release_date(self) -> str:
        return self._release_date

    @property
    def genre(self) -> str:
        return self._genre

    @property
    def album_name(self) -> str:
        return self._album_name

    @property
    def content_id(self) -> int:
        return self._content_id

    @property
    def collection_id(self) -> int:
        return self._collection_id

    @property
    def rating(self) -> str:
        return self._rating

    @property
    def media_kind(self) -> str:
        return self._media_kind

    @property
    def compilation(self) -> bool:
        return self._compilation

    @property
    def artwork_url(self) -> str:
        return self._album.artwork_url
