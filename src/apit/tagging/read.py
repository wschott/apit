from pathlib import Path

from . import format_registry
from apit.file_tags import FileTags


def read_tags(file: Path) -> FileTags:
    return format_registry.get_by(file).read(file)
