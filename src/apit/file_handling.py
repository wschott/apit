from collections.abc import Sequence
from pathlib import Path

from apit.utils.sort import sort_naturally


def collect_files(
    path: Path, filter_ext: Sequence[str] | str | None = None
) -> list[Path]:
    if path.is_file():
        unfiltered_files = [path]
    elif path.is_dir():
        unfiltered_files = [f for f in path.iterdir() if f.is_file()]

    sorted_files = sort_naturally(unfiltered_files)

    if not filter_ext:
        return sorted_files

    if isinstance(filter_ext, str):
        filter_ext = [filter_ext]

    return [f for f in sorted_files if f.suffix[1:] in filter_ext]
