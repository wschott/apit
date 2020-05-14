import urllib.error
from unittest.mock import MagicMock, patch

import pytest

from apit.error import ApitError
from apit.store.connection import (
    download_metadata,
    generate_metadata_lookup_url,
)

STORE_URL = 'https://music.apple.com/us/album/test-album/12345'
STORE_URL_COMPLEX = 'http://test.com/us/test/42/12345?i=09876/54321'
STORE_URL_ANYTHING = 'http://x/us/x/9/12345?i=09876'
STORE_URL_OLD = 'http://itunes.apple.com/us/album/test-album/id12345'
LOOKUP_URL = 'https://itunes.apple.com/lookup?entity=song&country=us&id=12345'


def test_generate_metadata_lookup_url_using_valid_url():
    assert generate_metadata_lookup_url(STORE_URL) == LOOKUP_URL


def test_generate_metadata_lookup_url_using_valid_old_url():
    assert generate_metadata_lookup_url(STORE_URL_OLD) == LOOKUP_URL


def test_generate_metadata_lookup_url_using_valid_random_url():
    assert generate_metadata_lookup_url(STORE_URL_COMPLEX) == LOOKUP_URL
    assert generate_metadata_lookup_url(STORE_URL_ANYTHING) == LOOKUP_URL


def test_generate_metadata_lookup_url_using_invalid_url():
    with pytest.raises(ApitError):
        generate_metadata_lookup_url('http://invalid-url.com/')


def test_download_metadata():
    response_attrs = {'read.return_value': b'{"resultCount":12, "results": [{}]}'}
    mock = MagicMock()
    mock.__enter__.return_value = MagicMock(**response_attrs)

    with patch('urllib.request.urlopen', return_value=mock):
        json = download_metadata(LOOKUP_URL)

    assert '{"resultCount":12, "results": [{}]}' == json


def test_download_metadata_with_http_error():
    with patch('urllib.request.urlopen', side_effect=urllib.error.HTTPError(url=None, code=500, msg='test-msg', hdrs=None, fp=None)):
        with pytest.raises(ApitError, match='due to HTTP error code "500": test-msg'):
            download_metadata(LOOKUP_URL)


def test_download_metadata_with_url_error():
    with patch('urllib.request.urlopen', side_effect=urllib.error.URLError('test-msg')):
        with pytest.raises(ApitError, match='due to error: test-msg'):
            download_metadata(LOOKUP_URL)
