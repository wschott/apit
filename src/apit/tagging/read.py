from pathlib import Path

import mutagen.mp4

from .mp4.constants import MP4_MAPPING
from .mp4.mp4_tag import Mp4Tag
from apit.error import ApitError
from apit.error import ApitNoTagsPresentError
from apit.file_tags import FileTags
from apit.tag_id import TagId

BLACKLIST: list[str] = [
    MP4_MAPPING.OWNER_NAME,
    MP4_MAPPING.USER_MAIL,
]


def read_tags(file: Path) -> FileTags:
    return to_file_tags(read_metadata_raw(file))


def read_metadata_raw(file: Path) -> mutagen.mp4.MP4:
    try:
        return mutagen.mp4.MP4(file)
    except mutagen.MutagenError as e:
        raise ApitError(e)


def to_file_tags(metadata_file: mutagen.mp4.MP4) -> FileTags:
    if not metadata_file.tags:
        raise ApitNoTagsPresentError()

    return FileTags(
        [Mp4Tag(TagId(tag), value) for tag, value in metadata_file.tags.items()]
    )


def is_itunes_bought_file(file: Path) -> bool:
    try:
        mp4_file = read_metadata_raw(file)
        if not mp4_file.tags:
            raise ApitNoTagsPresentError()
    except ApitError:
        return False
    else:
        return any(item in mp4_file.tags for item in BLACKLIST)
