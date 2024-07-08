import logging
import re
import urllib.error
import urllib.request
from typing import Final

from apit.errors import ApitError
from apit.errors import ApitStoreConnectionError
from apit.mime_type import MimeType
from apit.mime_type import to_mime_type

# format (as of 2020-05): https://music.apple.com/us/album/album-name/123456789
# old format: http://itunes.apple.com/us/album/album-name/id123456789
REGEX_STORE_URL: Final = re.compile(
    r"https?://[^/]*"
    + r"/(?P<country_code>[a-z]{2})"
    + r"/[^/]+/[^/]+"
    + r"/(id)?(?P<id>\d+)",
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
        with urllib.request.urlopen(url) as response:  # noqa: S310
            data_read = response.read()
            return data_read.decode("utf-8")
    except urllib.error.URLError as e:
        raise ApitStoreConnectionError(str(e))


def download_artwork(url: str) -> tuple[bytes, MimeType]:
    try:
        with urllib.request.urlopen(url) as response:  # noqa: S310
            content_type = response.getheader("Content-Type")
            logging.debug("Headers: %s", response.info())
            return response.read(), to_mime_type(content_type)
    except urllib.error.URLError as e:
        raise ApitStoreConnectionError(str(e))
