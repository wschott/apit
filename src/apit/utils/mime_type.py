from enum import Enum
from typing import Self


class MimeType(Enum):
    JPEG = "image/jpeg"
    PNG = "image/png"

    @classmethod
    def from_content_type(cls, content_type: str) -> Self:
        try:
            return cls(content_type)
        except ValueError:
            raise ValueError(f"Unknown content type: {content_type}")
