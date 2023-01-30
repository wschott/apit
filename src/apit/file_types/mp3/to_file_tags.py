import mutagen.mp3

from .mp3_tag import Mp3Tag
from apit.file_tags import FileTags
from apit.tag_id import TagId


def to_file_tags(metadata_file: mutagen.mp3.MP3) -> FileTags:
    if not metadata_file.tags:
        return FileTags([])

    return FileTags(
        [Mp3Tag(TagId(tag), value) for tag, value in metadata_file.tags.items()]
    )
