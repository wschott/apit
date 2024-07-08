import urllib.error
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from apit.errors import ApitError
from apit.errors import ApitStoreConnectionError
from apit.mime_type import MimeType
from apit.store.download import download_artwork
from apit.store.download import download_metadata
from apit.store.download import generate_lookup_url


@pytest.mark.parametrize(
    "url",
    [
        "https://music.apple.com/us/album/test-album/12345",  # Apple Music style
        "http://itunes.apple.com/us/album/test-album/id12345",  # old iTunes style
        "http://test.com/us/test/42/12345?i=09876/54321",  # complex url with query params
        "http://test/us/x/9/12345?i=09876",
    ],
)
def test_generate_lookup_url_valid_url(url: str):
    assert (
        generate_lookup_url(url)
        == "https://itunes.apple.com/lookup?entity=song&country=us&id=12345"
    )


@pytest.mark.parametrize(
    "url",
    [
        "http://invalid-url.com/",
        "https://music.apple.com/album/us/test-album/12345",
        "US,12345",
    ],
)
def test_generate_lookup_url_using_invalid_url(url: str):
    with pytest.raises(ApitError):
        generate_lookup_url(url)


def test_download_metadata():
    response_attrs = {"read.return_value": b'{"resultCount":12, "results": [{}]}'}
    mock = MagicMock()
    mock.__enter__.return_value = MagicMock(**response_attrs)

    with patch("urllib.request.urlopen", return_value=mock):
        json = download_metadata("any-url")

    assert json == '{"resultCount":12, "results": [{}]}'


def test_download_metadata_with_url_error():
    with (
        patch("urllib.request.urlopen", side_effect=urllib.error.URLError("test-msg")),
        pytest.raises(ApitStoreConnectionError, match="<urlopen error test-msg>"),
    ):
        download_metadata("any-url")

    with (
        patch(
            "urllib.request.urlopen",
            side_effect=urllib.error.HTTPError(
                url=None, code=500, msg="test-msg", hdrs=None, fp=None
            ),
        ),
        pytest.raises(ApitStoreConnectionError, match="HTTP Error 500: test-msg"),
    ):
        download_metadata("any-url")


def test_download_artwork():
    response_attrs = {
        "read.return_value": b"artwork-content",
        "info.return_value": "",
        "getheader.return_value": "image/jpeg",
    }
    mock = MagicMock()
    mock.__enter__.return_value = MagicMock(**response_attrs)

    with patch("urllib.request.urlopen", return_value=mock):
        artwork = download_artwork("any-url")

    assert b"artwork-content", artwork == MimeType.JPEG


def test_download_artwork_with_url_error():
    with (
        patch("urllib.request.urlopen", side_effect=urllib.error.URLError("test-msg")),
        pytest.raises(ApitStoreConnectionError, match="<urlopen error test-msg>"),
    ):
        download_artwork("any-url")

    with (
        patch(
            "urllib.request.urlopen",
            side_effect=urllib.error.HTTPError(
                url=None, code=500, msg="test-msg", hdrs=None, fp=None
            ),
        ),
        pytest.raises(ApitStoreConnectionError, match="HTTP Error 500: test-msg"),
    ):
        download_artwork("any-url")
