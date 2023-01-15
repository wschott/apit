from pathlib import Path

from .mp4 import MP4_MAPPING
from .mp4 import read_metadata_raw
from .mp4 import to_file_tags
from apit.error import ApitError
from apit.error import ApitNoTagsPresentError
from apit.file_tags import FileTags

BLACKLIST: list[str] = [
    MP4_MAPPING.OWNER_NAME,
    MP4_MAPPING.USER_MAIL,
]


def read_tags(file: Path) -> FileTags:
    return to_file_tags(read_metadata_raw(file))


def is_itunes_bought_file(file: Path) -> bool:
    try:
        mp4_file = read_metadata_raw(file)
        if not mp4_file.tags:
            raise ApitNoTagsPresentError()
    except ApitError:
        return False
    else:
        return any(item in mp4_file.tags for item in BLACKLIST)
