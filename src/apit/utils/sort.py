import re
from collections.abc import Iterable
from pathlib import Path


def sort_naturally(paths: Iterable[Path]) -> list[Path]:
    return sorted(paths, key=sort_naturally_key)


def sort_naturally_key(key: Path) -> list[int | str]:
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", str(key))]
