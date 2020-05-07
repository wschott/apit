from apit.error import ApitError
from apit.song import Song


class Album:
    def __init__(self, item):
        self.fields = item
        self.discs = {}

    def __getitem__(self, field):
        return self.fields[field]

    def hasDisc(self, disc_number: int) -> bool:
        return disc_number in self.discs

    def hasSong(self, track_number: int, disc_number: int) -> bool: # TODO = 1
        return self.hasDisc(disc_number) and track_number in self.discs[disc_number]

    def addSong(self, item: Song):
        if not self.hasDisc(item['discNumber']):
            self.discs[item['discNumber']] = {}

        self.discs[item['discNumber']][item['trackNumber']] = item

    def getSong(self, track_number: int, disc_number: int = 1) -> Song: # TODO = 1
        if not self.hasSong(track_number, disc_number):
            raise ApitError(f'No song found for disc {disc_number} and track {track_number}')

        return self.discs[disc_number][track_number]
