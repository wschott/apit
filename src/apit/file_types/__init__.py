from pathlib import Path

from apit.core.audio.audio_file import AudioFile
from apit.core.errors import ApitError
from apit.file_types.mp3 import Mp3File
from apit.file_types.mp4 import Mp4File

__all__ = ["AudioFileFactory"]


file_types: dict[str, type[AudioFile]] = {
    "m4a": Mp4File,
    "mp3": Mp3File,
}


class ApitUnsupportedFileTypeError(ApitError):
    def __init__(self, unsupported_type: str) -> None:
        super().__init__(f"Unsupported type: {unsupported_type}")


class AudioFileFactory:
    @classmethod
    def load(cls, file: Path) -> AudioFile:
        extension = file.suffix[1:]
        try:
            return file_types[extension](file)
        except KeyError as e:
            raise ApitUnsupportedFileTypeError(extension) from e

    @classmethod
    def get_supported_extensions(cls) -> list[str]:
        return list(file_types.keys())
