import os
import re
from pathlib import Path
from typing import List, Optional, Tuple, Union

REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME = re.compile(r'^[#]?((?P<disc>\d+)[-.])?(?P<track>\d+)[.]?.+')


def collect_files(path: Path, filter_ext: Optional[Union[List[str], str]] = None) -> List[Path]:
    # TODO handle non-existing folder
    unfiltered_files = [Path(f) for f in os.scandir(path) if f.is_file()]

    sorted_files = sorted(unfiltered_files)

    if not filter_ext:
        return sorted_files

    if isinstance(filter_ext, str):
        filter_ext = [filter_ext]

    return [f for f in sorted_files if f.suffix in filter_ext]


def extract_disc_and_track_number(path: Path) -> Tuple[int, int]:
    match = REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME.match(path.name)

    if not match:
        return None

    disc = match.groupdict()['disc'] if match.groupdict()['disc'] is not None else 1
    track = match.groupdict()['track']

    return int(disc), int(track)
