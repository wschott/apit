from collections import defaultdict
from typing import List, MutableMapping

from apit.error import ApitError

from .song import Song


class Album:
    def __init__(self, item):
        self.fields = item
        self.discs: MutableMapping[int, MutableMapping[int, Song]] = defaultdict(dict)

    def __getitem__(self, field):
        return self.fields[field]

    def has_disc(self, disc: int) -> bool:
        return int(disc) in self.discs

    def has_song(self, disc: int, track: int) -> bool:
        return self.has_disc(disc) and track in self.discs[disc]

    def add_song(self, song: Song) -> None:
        disc: int = song['discNumber']
        track: int = song['trackNumber']

        if self.has_song(disc=disc, track=track):
            raise ApitError('Adding a song with duplicate disc {} and track number is impossible')

        self.discs[disc][track] = song

    def get_song(self, disc: int, track: int) -> Song:
        if not self.has_song(disc=disc, track=track):
            raise ApitError(f'No song found for disc {disc} and track {track}')

        return self.discs[int(disc)][int(track)]

    def add_songs(self, songs: List[Song]) -> None:
        for song in songs:
            self.add_song(song)
