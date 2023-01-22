import logging
import re
import urllib.error
import urllib.request

from apit.error import ApitError
from apit.error import ApitStoreConnectionError
from apit.mime_type import MIME_TYPE

# format (as of 2020-05): https://music.apple.com/us/album/album-name/123456789
# old format: http://itunes.apple.com/us/album/album-name/id123456789
REGEX_GROUP_COUNTRY_CODE = r"(?P<country_code>[a-z]{2})"
REGEX_GROUP_ID = r"(?P<id>\d+)"

REGEX_STORE_URL = re.compile(
    r"https?://[^/]*/"
    + REGEX_GROUP_COUNTRY_CODE
    + r"/[^/]+/[^/]+/(id)?"
    + REGEX_GROUP_ID,
    re.IGNORECASE,
)


def generate_lookup_url(source: str) -> str:
    match = REGEX_STORE_URL.match(source)

    if not match:
        raise ApitError(f"Invalid URL format: {source}")

    country_code = match.groupdict()["country_code"]
    album_id = match.groupdict()["id"]
    return f"https://itunes.apple.com/lookup?entity=song&country={country_code}&id={album_id}"


def download_metadata(url: str) -> str:
    try:
        with urllib.request.urlopen(url) as response:
            data_read = response.read()
            return data_read.decode("utf-8")
    except urllib.error.URLError as e:
        raise ApitStoreConnectionError(str(e))


def download_artwork(url: str) -> tuple[bytes, MIME_TYPE]:
    try:
        with urllib.request.urlopen(url) as response:
            content_type = response.getheader("Content-Type")
            logging.debug("Headers: %s", response.info())
            return response.read(), _to_mime_type(content_type)
    except urllib.error.URLError as e:
        raise ApitStoreConnectionError(str(e))


def _to_mime_type(content_type: str) -> MIME_TYPE:
    try:
        return MIME_TYPE(content_type)
    except ValueError:
        raise ApitError(f"Unknown artwork content type: {content_type}")
