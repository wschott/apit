from datetime import datetime
from pathlib import Path

import mutagen.id3
import mutagen.mp3

from .constants import Mp3Mapping
from .read import read_metadata_raw
from apit.errors import ApitError
from apit.metadata import Artwork
from apit.metadata import Song
from apit.tag_id import TagId


def update_metadata(
    file: Path, song: Song, artwork: Artwork | None = None
) -> mutagen.mp3.MP3:
    mp3_file = read_metadata_raw(file)

    if mp3_file.tags is None:
        mp3_file.add_tags()

    _modify_mp3_file(mp3_file, song, artwork)
    # TODO error handling
    try:
        mp3_file.save()
    except Exception as e:
        raise ApitError(e)
    else:
        return mp3_file


def _to_artwork(artwork: Artwork) -> mutagen.id3.APIC:
    return mutagen.id3.APIC(
        mime=artwork.mimetype.value,
        type=mutagen.id3.PictureType.COVER_FRONT,
        data=artwork.content,
    )


def _modify_mp3_file(
    mp3_file: mutagen.mp3.MP3, song: Song, artwork: Artwork | None = None
) -> mutagen.mp3.MP3:
    _update_specific_tag(mp3_file.tags, Mp3Mapping.ARTIST, song.artist)
    _update_specific_tag(mp3_file.tags, Mp3Mapping.TITLE, song.title)
    _update_specific_tag(mp3_file.tags, Mp3Mapping.ALBUM_NAME, song.album_name)
    _update_specific_tag(mp3_file.tags, Mp3Mapping.GENRE, song.genre)
    _update_specific_tag(
        mp3_file.tags, Mp3Mapping.RELEASE_DATE, extract_year(song.release_date)
    )
    _update_specific_tag(
        mp3_file.tags, Mp3Mapping.DISC_NUMBER, f"{song.disc_number}/{song.disc_total}"
    )
    _update_specific_tag(
        mp3_file.tags,
        Mp3Mapping.TRACK_NUMBER,
        f"{song.track_number}/{song.track_total}",
    )
    _update_specific_tag(mp3_file.tags, Mp3Mapping.ALBUM_ARTIST, song.album_artist)
    _update_specific_tag(mp3_file.tags, Mp3Mapping.COPYRIGHT, song.copyright)
    if song.compilation:
        _update_specific_tag(
            mp3_file.tags, Mp3Mapping.COMPILATION, str(int(song.compilation))
        )
    else:
        _unset_tag(mp3_file.tags, Mp3Mapping.COMPILATION)

    if artwork:
        _update_artwork_tag(mp3_file.tags, Mp3Mapping.ARTWORK, artwork)

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


def _update_artwork_tag(tags, tag_id: TagId, artwork: Artwork):
    _unset_tag(tags, tag_id)
    apic = _to_artwork(artwork)
    tags.add(apic)


def _unset_tag(tags, tag_id: TagId):
    tags.delall(tag_id)
