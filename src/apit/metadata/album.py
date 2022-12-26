from dataclasses import dataclass


@dataclass
class Album:
    album_artist: str
    copyright: str
    artwork_url: str
