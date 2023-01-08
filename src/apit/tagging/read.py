from pathlib import Path

import mutagen.mp4

from apit.commands.show.reporting.file_tags import FileTags
from apit.commands.show.reporting.mp4.mp4_tag import Mp4Tag
from apit.error import ApitError
from apit.store.constants import BLACKLIST
from apit.tag_id import TagId


def read_metadata(file: Path) -> mutagen.mp4.MP4:
    try:
        return mutagen.mp4.MP4(file)
    except mutagen.MutagenError as e:
        raise ApitError(e)


def to_file_tags(metadata_file: mutagen.mp4.MP4) -> FileTags:
    if not metadata_file.tags:
        raise ApitError("No tags present")

    return FileTags(
        [Mp4Tag(TagId(tag), value) for tag, value in metadata_file.tags.items()]
    )


def is_itunes_bought_file(file: Path) -> bool:
    try:
        mp4_file = read_metadata(file)
        if not mp4_file.tags:
            raise ApitError("No tags present")
    except ApitError:
        return False
    else:
        return any(item in mp4_file.tags for item in BLACKLIST)
