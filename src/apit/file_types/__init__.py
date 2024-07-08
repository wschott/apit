from pathlib import Path

from apit.errors import ApitUnsupportedTypeError
from apit.file_types.audio_file import AudioFile
from apit.package_utils import load_entry_point_modules

__all__ = ["AudioFileFactory"]


file_types: dict[str, AudioFile] = load_entry_point_modules(group="apit.file_types")


class AudioFileFactory:
    @classmethod
    def load(cls, file: Path) -> AudioFile:
        extension = file.suffix[1:]
        try:
            return file_types[extension](file)  # type: ignore[operator]
        except KeyError as e:
            raise ApitUnsupportedTypeError(extension) from e

    @classmethod
    def get_supported_extensions(cls) -> list[str]:
        return list(file_types.keys())
