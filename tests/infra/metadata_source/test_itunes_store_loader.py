import urllib.error
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from apit.core.errors import ApitError
from apit.utils.http import ApitHttpConnectionError
from apit.infra.metadata_source.itunes_store_loader import ItunesStoreLoader
from apit.infra.metadata_source.itunes_store_loader import parse_store_url


@pytest.mark.parametrize(
    "url",
    [
        "https://music.apple.com/us/album/test-album/12345",  # Apple Music style
        "http://itunes.apple.com/us/album/test-album/id12345",  # old iTunes style
        "http://test.com/us/test/42/12345?i=09876/54321",  # complex url with query params
        "http://test/us/x/9/12345?i=09876",
    ],
)
def test_parse_store_url_valid_url(url: str):
    assert parse_store_url(url) == {"country_code": "us", "id": "12345"}


@pytest.mark.parametrize(
    "url",
    [
        "http://invalid-url.com/",
        "https://music.apple.com/album/us/test-album/12345",
        "US,12345",
    ],
)
def test_parse_store_url_using_invalid_url(url: str):
    with pytest.raises(ApitError):
        parse_store_url(url)


def test_download_metadata():
    response = MagicMock()
    response.read.return_value = b'{"resultCount":12, "results": [{}]}'
    mock = MagicMock()
    mock.__enter__.return_value = response

    with patch("urllib.request.urlopen", return_value=mock) as mock_urlopen:
        json = ItunesStoreLoader().download_metadata(
            {"country_code": "us", "id": "12345"}
        )

    assert json == '{"resultCount":12, "results": [{}]}'
    mock_urlopen.assert_called_once_with(
        "https://itunes.apple.com/lookup?entity=song&country=us&id=12345"
    )


def test_download_metadata_with_url_error():
    with (
        patch("urllib.request.urlopen", side_effect=urllib.error.URLError("test-msg")),
        pytest.raises(ApitHttpConnectionError, match="<urlopen error test-msg>"),
    ):
        ItunesStoreLoader().download_metadata({"country_code": "us", "id": "12345"})

    with (
        patch(
            "urllib.request.urlopen",
            side_effect=urllib.error.HTTPError(
                url="any-url",
                code=500,
                msg="test-msg",
                hdrs=None,  # ty: ignore[invalid-argument-type]
                fp=None,
            ),
        ),
        pytest.raises(ApitHttpConnectionError, match="HTTP Error 500: test-msg"),
    ):
        ItunesStoreLoader().download_metadata({"country_code": "us", "id": "12345"})


def test_download_artwork():
    response = MagicMock()
    response.read.return_value = b"artwork-content"
    response.info.return_value = ""
    response.getheader.return_value = "image/jpeg"
    mock = MagicMock()
    mock.__enter__.return_value = response

    with patch("urllib.request.urlopen", return_value=mock) as mock_urlopen:
        artwork = ItunesStoreLoader().download_artwork(
            "https://cover.url/img/100x100bb.jpg", 600
        )

    assert artwork == (b"artwork-content", "image/jpeg")
    mock_urlopen.assert_called_once_with("https://cover.url/img/600x600bb.jpg")


def test_download_artwork_with_url_error():
    with (
        patch("urllib.request.urlopen", side_effect=urllib.error.URLError("test-msg")),
        pytest.raises(ApitHttpConnectionError, match="<urlopen error test-msg>"),
    ):
        ItunesStoreLoader().download_artwork("any-url", 600)

    with (
        patch(
            "urllib.request.urlopen",
            side_effect=urllib.error.HTTPError(
                url="any-url",
                code=500,
                msg="test-msg",
                hdrs=None,  # ty: ignore[invalid-argument-type]
                fp=None,
            ),
        ),
        pytest.raises(ApitHttpConnectionError, match="HTTP Error 500: test-msg"),
    ):
        ItunesStoreLoader().download_artwork("any-url", 600)


def test_load_downloads_metadata(monkeypatch, test_metadata: str):
    monkeypatch.setattr(
        ItunesStoreLoader, "download_metadata", lambda self, album: test_metadata
    )

    metadata_json = ItunesStoreLoader().load(
        "https://music.apple.com/us/album/album-name/123456789"
    )

    assert metadata_json == test_metadata
