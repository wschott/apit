import os
from pathlib import Path


def save_metadata_to_cache(json: str, cache_file: Path) -> None:
    if not cache_file.parent.exists():
        os.makedirs(cache_file.parent)
    cache_file.write_text(json)


def save_artwork_to_cache(content: bytes, cache_file: Path) -> None:
    if not cache_file.parent.exists():
        os.makedirs(cache_file.parent)
    cache_file.write_bytes(content)
