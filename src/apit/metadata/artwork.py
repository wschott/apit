from dataclasses import dataclass
from dataclasses import field

from apit.mime_type import MIME_TYPE


@dataclass
class Artwork:
    content: bytes = field(repr=False)
    mimetype: MIME_TYPE
