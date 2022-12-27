# flake8: noqa: E221
import urllib.error
from unittest.mock import MagicMock, patch

import pytest

from apit.error import (
    ApitError,
    ApitStoreConnectionError,
    ApitSystemCountryCodeDeterminationError,
)
from apit.file_handling import MIME_TYPE
from apit.store.connection import (
    _to_mime_type,
    download_artwork,
    download_metadata,
    generate_lookup_url_by_str,
    generate_lookup_url_by_url,
)

# fmt: off
STORE_URL           = 'https://music.apple.com/us/album/test-album/12345'
STORE_URL_INVALID   = 'https://music.apple.com/album/us/test-album/12345'
STORE_URL_COMPLEX   = 'http://test.com/us/test/42/12345?i=09876/54321'
STORE_URL_ANYTHING  = 'http://test/us/x/9/12345?i=09876'
STORE_URL_OLD       = 'http://itunes.apple.com/us/album/test-album/id12345'
LOOKUP_URL          = 'https://itunes.apple.com/lookup?entity=song&country=us&id=12345'
LOOKUP_URL_NON_US   = 'https://itunes.apple.com/lookup?entity=song&country=xy&id=12345'
ARTWORK_URL         = 'https://is1-ssl.mzstatic.com/image/thumb/Music128/v4/12/12/12/12345678-1234-1234-1234-123456781234/source/600x600bb.jpg'
# fmt: on


def test_generate_lookup_url_by_url_using_valid_url():
    assert generate_lookup_url_by_url(STORE_URL) == LOOKUP_URL


def test_generate_lookup_url_by_url_using_valid_old_url():
    assert generate_lookup_url_by_url(STORE_URL_OLD) == LOOKUP_URL


def test_generate_lookup_url_by_url_using_valid_random_url():
    assert generate_lookup_url_by_url(STORE_URL_COMPLEX) == LOOKUP_URL
    assert generate_lookup_url_by_url(STORE_URL_ANYTHING) == LOOKUP_URL


def test_generate_lookup_url_by_url_using_invalid_url():
    with pytest.raises(ApitError):
        generate_lookup_url_by_url("http://invalid-url.com/")
    with pytest.raises(ApitError):
        generate_lookup_url_by_url(STORE_URL_INVALID)


def test_generate_lookup_url_by_str():
    assert generate_lookup_url_by_str("US,12345") == LOOKUP_URL
    assert generate_lookup_url_by_str("us.12345") == LOOKUP_URL


def test_generate_lookup_url_by_str_invalid():
    with pytest.raises(ApitError):
        generate_lookup_url_by_str(",12345")


def test_generate_lookup_url_by_str_using_locale(monkeypatch):
    monkeypatch.setattr("locale.getdefaultlocale", lambda: ("ab_XY", "uft8"))
    assert generate_lookup_url_by_str("12345") == LOOKUP_URL_NON_US


def test_generate_lookup_url_by_str_using_invalid_locale(monkeypatch):
    monkeypatch.setattr("locale.getdefaultlocale", lambda: ("XY", "uft8"))
    with pytest.raises(ApitSystemCountryCodeDeterminationError):
        generate_lookup_url_by_str("12345")


def test_download_metadata():
    response_attrs = {"read.return_value": b'{"resultCount":12, "results": [{}]}'}
    mock = MagicMock()
    mock.__enter__.return_value = MagicMock(**response_attrs)

    with patch("urllib.request.urlopen", return_value=mock):
        json = download_metadata(LOOKUP_URL)

    assert '{"resultCount":12, "results": [{}]}' == json


def test_download_metadata_with_url_error():
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("test-msg")):
        with pytest.raises(ApitStoreConnectionError, match="<urlopen error test-msg>"):
            download_metadata(LOOKUP_URL)
    with patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.HTTPError(
            url=None, code=500, msg="test-msg", hdrs=None, fp=None
        ),
    ):
        with pytest.raises(ApitStoreConnectionError, match="HTTP Error 500: test-msg"):
            download_metadata(LOOKUP_URL)


def test_download_artwork():
    response_attrs = {
        "read.return_value": b"artwork-content",
        "info.return_value": "",
        "getheader.return_value": "image/jpeg",
    }
    mock = MagicMock()
    mock.__enter__.return_value = MagicMock(**response_attrs)

    with patch("urllib.request.urlopen", return_value=mock):
        artwork = download_artwork(ARTWORK_URL)

    assert b"artwork-content", MIME_TYPE.JPEG == artwork


def test_download_artwork_with_url_error():
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("test-msg")):
        with pytest.raises(ApitStoreConnectionError, match="<urlopen error test-msg>"):
            download_artwork(ARTWORK_URL)
    with patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.HTTPError(
            url=None, code=500, msg="test-msg", hdrs=None, fp=None
        ),
    ):
        with pytest.raises(ApitStoreConnectionError, match="HTTP Error 500: test-msg"):
            download_artwork(ARTWORK_URL)


def test_to_mime_type():
    assert _to_mime_type("image/jpeg") == MIME_TYPE.JPEG
    assert _to_mime_type("image/png") == MIME_TYPE.PNG


def test_to_mime_type_for_unknown_type():
    with pytest.raises(ApitError, match="Unknown artwork content type: test-type"):
        _to_mime_type("test-type")
