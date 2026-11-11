import logging
import urllib.error
import urllib.request
from urllib.parse import urlparse

from apit.core.errors import ApitError


class ApitHttpConnectionError(ApitError):
    pass


def download(url: str) -> tuple[bytes, str]:
    try:
        with urllib.request.urlopen(url) as response:  # noqa: S310
            content = response.read()
            content_type = response.getheader("Content-Type")
            logging.debug("Headers: %s", response.info())
            return content, content_type
    except urllib.error.URLError as e:
        raise ApitHttpConnectionError(
            f"Connection to Apple Music/iTunes Store failed due to error: ${e!s}"
        )


def is_url(url: str) -> bool:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
