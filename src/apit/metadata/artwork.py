from dataclasses import dataclass
from dataclasses import field

from apit.mime_type import MimeType


@dataclass
class Artwork:
    content: bytes = field(repr=False)
    mimetype: MimeType
