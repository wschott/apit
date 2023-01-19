from datetime import datetime
from pathlib import Path

import mutagen.id3
import mutagen.mp3

from .constants import MP3_MAPPING
from .read import read_metadata_raw
from apit.error import ApitError
from apit.file_handling import MIME_TYPE
from apit.metadata import Song
from apit.tag_id import TagId

ARTWORK_FORMATS = {
    ".jpg": MIME_TYPE.JPEG.value,
    ".png": MIME_TYPE.PNG.value,
}


def update_metadata(
    file: Path, song: Song, cover_path: Path | None = None
) -> mutagen.mp3.MP3:
    mp3_file = read_metadata_raw(file)

    if mp3_file.tags is None:
        mp3_file.add_tags()

    if cover_path:
        artwork = _read_artwork_content(cover_path)
        _modify_mp3_file(mp3_file, song, artwork)
    else:
        _modify_mp3_file(mp3_file, song)
    # TODO error handling
    try:
        mp3_file.save()
    except Exception as e:
        raise ApitError(e)
    else:
        return mp3_file


def _read_artwork_content(artwork_path: Path) -> mutagen.id3.APIC:
    try:
        image_format = ARTWORK_FORMATS[artwork_path.suffix]
    except KeyError:
        raise ApitError(f"Unknown artwork image type: {artwork_path.suffix}")
    else:
        return mutagen.id3.APIC(
            mime=image_format,
            type=mutagen.id3.PictureType.COVER_FRONT,
            data=artwork_path.read_bytes(),
        )


def _modify_mp3_file(
    mp3_file: mutagen.mp3.MP3, song: Song, artwork: mutagen.id3.APIC | None = None
) -> mutagen.mp3.MP3:
    _update_specific_tag(mp3_file.tags, MP3_MAPPING.ARTIST, song.artist)
    _update_specific_tag(mp3_file.tags, MP3_MAPPING.TITLE, song.title)
    _update_specific_tag(mp3_file.tags, MP3_MAPPING.ALBUM_NAME, song.album_name)
    _update_specific_tag(mp3_file.tags, MP3_MAPPING.GENRE, song.genre)
    _update_specific_tag(
        mp3_file.tags, MP3_MAPPING.RELEASE_DATE, extract_year(song.release_date)
    )
    _update_specific_tag(
        mp3_file.tags, MP3_MAPPING.DISC_NUMBER, f"{song.disc_number}/{song.disc_total}"
    )
    _update_specific_tag(
        mp3_file.tags,
        MP3_MAPPING.TRACK_NUMBER,
        f"{song.track_number}/{song.track_total}",
    )
    _update_specific_tag(mp3_file.tags, MP3_MAPPING.ALBUM_ARTIST, song.album_artist)
    _update_specific_tag(mp3_file.tags, MP3_MAPPING.COPYRIGHT, song.copyright)
    if song.compilation:
        _update_specific_tag(
            mp3_file.tags, MP3_MAPPING.COMPILATION, str(int(song.compilation))
        )
    else:
        _unset_tag(mp3_file.tags, MP3_MAPPING.COMPILATION)

    if artwork:
        _update_artwork_tag(mp3_file.tags, MP3_MAPPING.ARTWORK, artwork)

    return mp3_file


def extract_year(date: str) -> str:
    return str(datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").year)


def _update_specific_tag(tags, tag_id: TagId, value):
    try:
        tag = tags[tag_id]
    except KeyError:
        tags.add(mutagen.id3.Frames[tag_id](encoding=3, text=value))
    else:
        tag.encoding = 3
        tag.text = value


def _update_artwork_tag(tags, tag_id: TagId, value):
    _unset_tag(tags, tag_id)
    tags.add(value)


def _unset_tag(tags, tag_id: TagId):
    tags.delall(tag_id)
