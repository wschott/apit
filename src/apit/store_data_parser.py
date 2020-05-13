import json
from typing import List

from apit.error import ApitError
from apit.metadata import Album, Song


def extract_album_with_songs(metadata_json: str) -> Album:
    try:
        itunes_data = json.loads(metadata_json)
    except json.JSONDecodeError:
        raise ApitError('Apple Music/iTunes Store metadata results format error')

    if 'results' not in itunes_data or 'resultCount' not in itunes_data or itunes_data['resultCount'] == 0:
        raise ApitError('Apple Music/iTunes Store metadata results empty')

    return _find_album_with_songs(itunes_data['results'])


def _find_album_with_songs(music_data) -> Album:
    album = _find_album(music_data)
    album.add_songs(_find_songs(music_data))
    return album


def _find_album(music_data) -> Album:
    for item in music_data:
        if 'collectionType' in item and item['collectionType'] in ['Album', 'Compilation']:
            return Album(item)
    raise ApitError('No album found in metadata')


def _find_songs(music_data) -> List[Song]:
    return [Song(item) for item in music_data if 'kind' in item and item['kind'] == 'song']
