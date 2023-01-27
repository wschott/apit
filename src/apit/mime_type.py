from enum import Enum

from apit.error import ApitError


class MimeType(Enum):
    JPEG = "image/jpeg"
    PNG = "image/png"


def to_mime_type(content_type: str) -> MimeType:
    try:
        return MimeType(content_type)
    except ValueError:
        raise ApitError(f"Unknown content type: {content_type}")
