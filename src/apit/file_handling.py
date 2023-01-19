import os
import re
from collections.abc import Iterable
from pathlib import Path

from apit.sort import sort_naturally

REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME = re.compile(
    r"^[#]?((?P<disc>\d+)[-.])?(?P<track>\d+)"
)


def collect_files(
    path: Path, filter_ext: Iterable[str] | str | None = None
) -> list[Path]:
    if path.is_file():
        unfiltered_files = [path]
    elif path.is_dir():
        unfiltered_files = [Path(f) for f in os.scandir(path) if f.is_file()]

    sorted_files = sort_naturally(unfiltered_files)

    if not filter_ext:
        return sorted_files

    if isinstance(filter_ext, str):
        filter_ext = [filter_ext]

    return [f for f in sorted_files if f.suffix[1:] in filter_ext]


def extract_disc_and_track_number(path: Path) -> tuple[int | None, int | None]:
    match = REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME.match(path.name)

    if not match:
        return None, None

    disc = (
        int(match.groupdict()["disc"]) if match.groupdict()["disc"] is not None else 1
    )
    track = int(match.groupdict()["track"])

    return disc, track
