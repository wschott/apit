import re
from collections.abc import Iterable
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from enum import auto
from pathlib import Path
from typing import Final

from apit.core.metadata.disc_number import DiscNumber
from apit.core.metadata.track_number import TrackNumber
from apit.core.metadata.song import Song
from apit.utils.text import clean
from apit.utils.text import compare_normalized_caseless

REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME: Final = re.compile(
    r"^[#]?((?P<disc>\d+)[-.])?(?P<track>\d+)"
)


def extract_disc_number(path: Path) -> DiscNumber | None:
    match = REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME.match(path.name)
    if match is None or match.group("disc") is None:
        return None

    return DiscNumber(int(match.group("disc")))


def extract_track_number(path: Path) -> TrackNumber | None:
    if (match := REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME.match(path.name)) is None:
        return None

    return TrackNumber(int(match.group("track")))


def find_song(
    songs: Iterable[Song], disc: DiscNumber | None, track: TrackNumber | None
) -> Song | None:
    for song in songs:
        if song.disc_number == disc and song.track_number == track:
            return song
    return None  # TODO raise?


def filename_matches_song(file: Path, song: Song) -> bool:
    filename_without_track_number = REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME.sub(
        "", str(file.with_suffix("").name)
    )

    return compare_normalized_caseless(
        clean(filename_without_track_number),
        clean(song.title),
    )


class MatchQuality(Enum):
    EXACT = auto()
    DIFFERS = auto()
    NONE = auto()


class SkipReason(Enum):
    NO_TRACK_NUMBER = auto()
    NO_METADATA = auto()


@dataclass(frozen=True)
class Match:
    file: Path
    song: Song | None
    quality: MatchQuality
    skip_reason: SkipReason | None

    @property
    def actionable(self) -> bool:
        return self.song is not None


def match(files: Iterable[Path], songs: Sequence[Song]) -> list[Match]:
    return [_match_file(file, songs) for file in files]


def _match_file(file: Path, songs: Sequence[Song]) -> Match:
    disc = extract_disc_number(file)
    if disc is None:
        disc = DiscNumber(1)
    track = extract_track_number(file)
    if not (disc and track):
        return Match(file, None, MatchQuality.NONE, SkipReason.NO_TRACK_NUMBER)

    song = find_song(songs, disc=disc, track=track)
    if song is None:
        return Match(file, None, MatchQuality.NONE, SkipReason.NO_METADATA)

    quality = (
        MatchQuality.EXACT
        if filename_matches_song(file, song)
        else MatchQuality.DIFFERS
    )
    return Match(file, song, quality, None)
