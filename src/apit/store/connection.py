import re
import urllib.error
import urllib.request

from apit.error import ApitError

# format (as of 2020-05): https://music.apple.com/us/album/album-name/123456789
# old format: http://itunes.apple.com/us/album/album-name/id123456789
REGEX_GROUP_COUNTRY_CODE = r'(?P<country_code>[a-z]{2})'
REGEX_GROUP_ID = r'(?P<id>\d+)'

REGEX_STORE_URL = re.compile(
    r'https?://[^/]*/' + REGEX_GROUP_COUNTRY_CODE + r'/[^/]+/[^/]+/(id)?' + REGEX_GROUP_ID,
    re.IGNORECASE)
ID_WITH_OPTIONAL_COUNTRY_CODE_AND_SEPARATOR = re.compile(
    r'(' + REGEX_GROUP_COUNTRY_CODE + r'[^a-z0-9]?)?' + REGEX_GROUP_ID,
    re.IGNORECASE)
LANGUAGE_COUNTRY_REGEX = re.compile(
    r'[a-z]{2}_' + REGEX_GROUP_COUNTRY_CODE,
    re.IGNORECASE)


def generate_lookup_url_by_url(source: str) -> str:
    match = REGEX_STORE_URL.match(source)

    if not match:
        raise ApitError(f'Invalid URL format: {source}')

    country_code = match.groupdict()['country_code']
    album_id = match.groupdict()['id']
    return _generate_metadata_lookup_url(album_id, country_code)


def generate_lookup_url_by_str(source: str) -> str:
    match = ID_WITH_OPTIONAL_COUNTRY_CODE_AND_SEPARATOR.match(source)

    if not match:
        raise ApitError(f'Invalid URL format: {source}')

    if match.groupdict()['country_code']:
        # user has provided country code
        country_code = match.groupdict()['country_code']
    else:
        country_code = determine_system_country_code()

    country_code = country_code.lower()
    album_id = match.groupdict()['id']
    return _generate_metadata_lookup_url(album_id, country_code)


def _generate_metadata_lookup_url(album_id: str, country_code: str) -> str:
    return f'https://itunes.apple.com/lookup?entity=song&country={country_code}&id={album_id}'


def determine_system_country_code() -> str:
    import locale
    system_language, _ = locale.getdefaultlocale()
    country_match = LANGUAGE_COUNTRY_REGEX.match(system_language)
    if not country_match:
        raise ApitError('Impossible to determine system country code. Use another possibility as metadata input source')
    return country_match.groupdict()['country_code']


def download_metadata(url: str) -> str:
    try:
        with urllib.request.urlopen(url) as response:
            data_read = response.read()
            return data_read.decode('utf-8')
    except urllib.error.HTTPError as e:
        raise ApitError('Connection to Apple Music/iTunes Store failed due to HTTP error code "%d": %s' % (e.code, e.reason))
    except urllib.error.URLError as e:
        raise ApitError('Connection to Apple Music/iTunes Store failed due to error: %s' % e.reason)
