from pathlib import Path

from .mp4 import read_metadata_raw
from .mp4 import to_file_tags
from apit.file_tags import FileTags


def read_tags(file: Path) -> FileTags:
    return to_file_tags(read_metadata_raw(file))
