from pathlib import Path

import mutagen.mp3

from apit.errors import ApitError


def read_metadata_raw(file: Path) -> mutagen.mp3.MP3:
    try:
        return mutagen.mp3.MP3(file)
    except mutagen.MutagenError as e:
        raise ApitError(e)
