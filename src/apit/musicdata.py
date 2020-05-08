import json
import re
import urllib.request
from typing import Any, List

from apit.album import Album
from apit.error import ApitError
from apit.song import Song

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

def fetch_store_json_string(url: str) -> str:
    openUrl = urllib.request.urlopen(url)
    if openUrl.getcode() != 200:
        raise ApitError('Connection to Apple Music/iTunes Store failed with error code: %s' % openUrl.getcode())
    return openUrl.read()

def extract_album_and_song_data(metadata_json: str) -> Album:
    itunes_data = json.loads(metadata_json)

    if 'results' not in itunes_data or 'resultCount' not in itunes_data or itunes_data['resultCount'] == 0:
        raise ApitError('Apple Music/iTunes Store metadata results empty')

    return _find_album_data(itunes_data['results'])

def _find_album_data(music_data: List[Any]) -> Album:
    album: Album
    for item in music_data:
        if 'collectionType' in item and item['collectionType'] in ['Album', 'Compilation']:
            album = Album(item)
            break

    if album:
        for item in music_data:
            if 'kind' in item and item['kind'] == 'song':
                album.addSong(Song(item))

    return album
