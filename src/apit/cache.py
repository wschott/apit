from pathlib import Path

from apit.file_handling import ensure_folder_exists


def save_metadata_to_cache(json: str, cache_file: Path) -> None:
    ensure_folder_exists(cache_file)
    cache_file.write_text(json)


def save_artwork_to_cache(content: bytes, cache_file: Path) -> None:
    ensure_folder_exists(cache_file)
    cache_file.write_bytes(content)
