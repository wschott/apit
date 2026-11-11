import logging
import re
from typing import Final
from typing import TypedDict
from typing import override

from apit.core.errors import ApitError
from apit.core.metadata_loader import MetadataLoader
from apit.utils.http import download


# format (as of 2020-05): https://music.apple.com/us/album/album-name/123456789
# old format: http://itunes.apple.com/us/album/album-name/id123456789
REGEX_STORE_URL: Final = re.compile(
    r"https?://[^/]*"
    + r"/(?P<country_code>[a-z]{2})"
    + r"/[^/]+/[^/]+"
    + r"/(id)?(?P<id>\d+)",
    re.IGNORECASE,
)


class StoreAlbumId(TypedDict):
    country_code: str
    id: str


def parse_store_url(source: str) -> StoreAlbumId:
    match = REGEX_STORE_URL.match(source)

    if not match:
        raise ApitError(f"Invalid URL format: {source}")

    return StoreAlbumId(
        country_code=match.group("country_code"),
        id=match.group("id"),
    )


class ItunesStoreLoader(MetadataLoader):
    @override
    def load(self, source: str) -> str:
        logging.info("Use URL to download metadata: %s", source)
        store_album_id = parse_store_url(source)
        return self.download_metadata(store_album_id)

    def download_metadata(self, album: StoreAlbumId) -> str:
        url = f"https://itunes.apple.com/lookup?entity=song&country={album['country_code']}&id={album['id']}"
        logging.info("Query URL: %s", url)
        content, _ = download(url)
        return content.decode("utf-8")

    def download_artwork(self, url: str, size: int) -> tuple[bytes, str]:
        scaled_artwork_url = url.replace("100x100", f"{size}x{size}")
        return download(scaled_artwork_url)
