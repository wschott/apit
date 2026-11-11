from dataclasses import dataclass
from dataclasses import field

from apit.utils.mime_type import MimeType


@dataclass
class Artwork:
    content: bytes = field(repr=False)
    mime_type: MimeType
