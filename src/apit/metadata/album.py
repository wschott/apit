class Album:
    def __init__(self,
                 album_artist: str,
                 copyright: str,
                 artwork_url: str,
                 ):
        self._album_artist = album_artist
        self._copyright = copyright
        self._artwork_url = artwork_url

    @property
    def album_artist(self) -> str:
        return self._album_artist

    @property
    def copyright(self) -> str:
        return self._copyright

    @property
    def artwork_url(self) -> str:
        return self._artwork_url
