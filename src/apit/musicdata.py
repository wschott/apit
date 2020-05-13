import json
import re
import urllib.request
from typing import List

from apit.error import ApitError
from apit.metadata import Album, Song

# format (as of 2020-05): https://music.apple.com/us/album/album-name/123456789
# old format: http://itunes.apple.com/us/album/album-name/id123456789
REGEX_STORE_URL_COUNTRY_CODE_ID = re.compile(r'^https?:\/\/[^\/]*\/(?P<country_code>[a-z]{2})\/[^\/]+\/[^\/]+\/(id)?(?P<id>\d+)')


def generate_store_lookup_url(user_url: str) -> str:
    match = REGEX_STORE_URL_COUNTRY_CODE_ID.match(user_url)

    if not match:
        raise ApitError(f'Invalid URL format: {user_url}')

    country_code = match.groupdict()['country_code']
    album_id = match.groupdict()['id']
    return f'https://itunes.apple.com/lookup?entity=song&country={country_code}&id={album_id}'


def fetch_store_json(url: str) -> str:
    open_url = urllib.request.urlopen(url)
    if open_url.getcode() != 200:
        raise ApitError('Connection to Apple Music/iTunes Store failed with error code: %s' % open_url.getcode())
    return open_url.read()


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
