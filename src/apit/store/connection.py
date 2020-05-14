import re
import urllib.error
import urllib.request

from apit.error import ApitError

# format (as of 2020-05): https://music.apple.com/us/album/album-name/123456789
# old format: http://itunes.apple.com/us/album/album-name/id123456789
REGEX_STORE_URL_COUNTRY_CODE_ID = re.compile(r'^https?:\/\/[^\/]*\/(?P<country_code>[a-z]{2})\/[^\/]+\/[^\/]+\/(id)?(?P<id>\d+)')


def generate_metadata_lookup_url(user_url: str) -> str:
    match = REGEX_STORE_URL_COUNTRY_CODE_ID.match(user_url)

    if not match:
        raise ApitError(f'Invalid URL format: {user_url}')

    country_code = match.groupdict()['country_code']
    album_id = match.groupdict()['id']
    return f'https://itunes.apple.com/lookup?entity=song&country={country_code}&id={album_id}'


def download_metadata(url: str) -> str:
    try:
        with urllib.request.urlopen(url) as response:
            data_read = response.read()
            return data_read.decode('utf-8')
    except urllib.error.HTTPError as e:
        raise ApitError('Connection to Apple Music/iTunes Store failed due to HTTP error code "%d": %s' % (e.code, e.reason))
    except urllib.error.URLError as e:
        raise ApitError('Connection to Apple Music/iTunes Store failed due to error: %s' % e.reason)
