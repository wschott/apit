import mutagen.mp4

from .mp4_tag import Mp4Tag
from apit.file_tags import FileTags
from apit.tag_id import TagId


def to_file_tags(metadata_file: mutagen.mp4.MP4) -> FileTags:
    if not metadata_file.tags:
        return FileTags([])

    return FileTags(
        [Mp4Tag(TagId(tag), value) for tag, value in metadata_file.tags.items()]
    )
