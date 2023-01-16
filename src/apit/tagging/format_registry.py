from collections.abc import MutableMapping
from pathlib import Path

from .format import Format
from apit.error import ApitUnsupportedFileTypeError


class FormatRegistry:
    def __init__(self) -> None:
        self._ext_to_format_map: MutableMapping[str, type[Format]] = {}

    def register(self, format: type[Format]) -> None:
        for extension in format.extensions:
            self._ext_to_format_map[extension] = format

    def get_by(self, file: Path) -> type[Format]:
        extension = file.suffix[1:]
        try:
            return self._ext_to_format_map[extension]
        except KeyError:
            raise ApitUnsupportedFileTypeError(extension)

    def get_supported_extensions(self) -> list[str]:
        return list(self._ext_to_format_map.keys())
