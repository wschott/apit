from pathlib import Path

from .format import Format
from apit.file_tags import FileTags


def read_tags(file: Path) -> FileTags:
    return Format.get_by(file).read(file)
