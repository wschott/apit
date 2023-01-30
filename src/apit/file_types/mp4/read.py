from pathlib import Path

import mutagen.mp4

from apit.errors import ApitError


def read_metadata_raw(file: Path) -> mutagen.mp4.MP4:
    try:
        return mutagen.mp4.MP4(file)
    except mutagen.MutagenError as e:
        raise ApitError(e)
