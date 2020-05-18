import os
from pathlib import Path


def save_to_cache(json: str, cache_file: Path) -> None:
    if not cache_file.parent.exists():
        os.makedirs(cache_file.parent)
    cache_file.write_text(json)
