import os
import re
from collections.abc import Sequence
from enum import Enum
from pathlib import Path

from apit.error import ApitError
from apit.metadata import Song

REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME = re.compile(
    r"^[#]?((?P<disc>\d+)[-.])?(?P<track>\d+).+"
)


class MIME_TYPE(Enum):
    JPEG = "image/jpeg"
    PNG = "image/png"


MIME_TPYE_TO_EXTENSION_MAP = {
    MIME_TYPE.JPEG: "jpg",
    MIME_TYPE.PNG: "png",
}


def collect_files(
    path_string: str, filter_ext: Sequence[str] | str | None = None
) -> list[Path]:
    path = Path(path_string).expanduser()

    if not path.exists():
        raise ApitError(f"Invalid path: {path}")

    if path.is_file():
        unfiltered_files = [path]
    elif path.is_dir():
        unfiltered_files = [Path(f) for f in os.scandir(path) if f.is_file()]

    sorted_files = sorted(unfiltered_files)

    if not filter_ext:
        return sorted_files

    if isinstance(filter_ext, str):
        filter_ext = [filter_ext]

    return [f for f in sorted_files if f.suffix in filter_ext]


def extract_disc_and_track_number(path: Path) -> tuple[int, int] | None:
    match = REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME.match(path.name)

    if not match:
        return None

    disc = (
        int(match.groupdict()["disc"]) if match.groupdict()["disc"] is not None else 1
    )
    track = int(match.groupdict()["track"])

    return disc, track


def generate_cache_filename(cache_path: Path, song: Song) -> Path:
    filename_prefix = _generate_filename_prefix(song)
    return cache_path / f"{filename_prefix}.json"


def generate_artwork_filename(
    cache_path: Path, song: Song, image_type: MIME_TYPE
) -> Path:
    filename_prefix = _generate_filename_prefix(song)
    suffix = MIME_TPYE_TO_EXTENSION_MAP[image_type]
    return cache_path / f"{filename_prefix}.{suffix}"


def _generate_filename_prefix(song: Song) -> str:
    filename_parts = [
        song.album_artist,
        song.album_name,
        song.collection_id,
    ]
    filename: list[str] = [re.sub(r"\W+", "_", str(f)) for f in filename_parts]
    return "-".join(filename)


def ensure_folder_exists(file_path: Path) -> None:
    if not file_path.parent.exists():
        os.makedirs(file_path.parent)
