class Album:
    def __init__(self, album_artist: str, copyright: str):
        self._album_artist = album_artist
        self._copyright = copyright

    @property
    def album_artist(self) -> str:
        return self._album_artist

    @property
    def copyright(self) -> str:
        return self._copyright
