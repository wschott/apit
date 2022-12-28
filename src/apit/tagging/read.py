from pathlib import Path

import mutagen.mp4

from apit.error import ApitError
from apit.store.constants import BLACKLIST


def read_metadata(file: Path) -> mutagen.mp4.MP4:
    try:
        return mutagen.mp4.MP4(file)
    except mutagen.MutagenError as e:
        raise ApitError(e)


def is_itunes_bought_file(file: Path) -> bool:
    try:
        mp4_file = read_metadata(file)
        if not mp4_file.tags:
            raise ApitError("No tags present")
    except ApitError:
        return False
    else:
        return any(item in mp4_file.tags for item in BLACKLIST)
