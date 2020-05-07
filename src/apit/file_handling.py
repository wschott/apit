import os
import re
from pathlib import Path
from typing import List, Optional, Tuple, Union

from apit.error import ApitError

REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME = r'^(?:(?P<disc_number>\d+)-)?(?P<track_number>\d+).+'

def get_files(path: Path, filter_ext: Optional[Union[List[str], str]] = None) -> List[Path]:
    unfiltered_files = [Path(f) for f in os.scandir(path) if f.is_file()]

    sorted_files = sorted(unfiltered_files)

    if not filter_ext:
        return sorted_files

    if isinstance(filter_ext, str):
        filter_ext = [filter_ext]

    return [f for f in sorted_files if f.suffix in filter_ext]

def extract_disc_and_track_number(path: Path) -> Tuple[int, int]:
    match = re.match(REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME, path.name)

    if not match:
        raise ApitError(f'Invalid filename format: {path}')

    disc = int(match.groupdict()['disc_number'] if match.groupdict()['disc_number'] is not None else 1)
    track = int(match.groupdict()['track_number'])

    return disc, track
