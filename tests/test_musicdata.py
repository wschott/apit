import json
from unittest.mock import patch, MagicMock

import pytest

from apit.error import ApitError
from apit.musicdata import (
    extract_album_with_songs,
    fetch_store_json,
    generate_store_lookup_url,
)

STORE_URL = 'https://music.apple.com/us/album/test-album/12345'
STORE_URL_COMPLEX = 'http://test.com/us/test/42/12345?i=09876/54321'
STORE_URL_ANYTHING = 'http://x/us/x/9/12345?i=09876'
STORE_URL_OLD = 'http://itunes.apple.com/us/album/test-album/id12345'
LOOKUP_URL = 'https://itunes.apple.com/lookup?entity=song&country=us&id=12345'


def test_generate_store_lookup_url_using_valid_url():
    assert generate_store_lookup_url(STORE_URL) == LOOKUP_URL


def test_generate_store_lookup_url_using_valid_old_url():
    assert generate_store_lookup_url(STORE_URL_OLD) == LOOKUP_URL


def test_generate_store_lookup_url_using_valid_random_url():
    assert generate_store_lookup_url(STORE_URL_COMPLEX) == LOOKUP_URL
    assert generate_store_lookup_url(STORE_URL_ANYTHING) == LOOKUP_URL


def test_generate_store_lookup_url_using_invalid_url():
    with pytest.raises(ApitError):
        generate_store_lookup_url('http://invalid-url.com/')


def test_extract_album_with_songs(test_metadata):
    album = extract_album_with_songs(test_metadata)

    assert album['collectionId'] == 1440742903
    assert album['artistName'] == 'Kanye West'
    assert album['collectionName'] == 'My Beautiful Dark Twisted Fantasy'

    song = album.get_song(disc=1, track=3)
    assert song['kind'] == 'song'
    assert song['discNumber'] == 1
    assert song['trackNumber'] == 3
    assert song['trackName'] == 'Power'


def test_extract_album_with_songs_invalid_json():
    with pytest.raises(ApitError):
        extract_album_with_songs('')
    with pytest.raises(ApitError):
        extract_album_with_songs('{"test":[], "resultCount": 0}')
    with pytest.raises(ApitError):
        extract_album_with_songs('{"results":[], "test": 0}')
    with pytest.raises(ApitError):
        extract_album_with_songs('{"results":[], "resultCount": 0}')


def test_fetch_store_json():
    mock_response = MagicMock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = b'{"resultCount":12, "results": [{}]}'

    with patch('urllib.request.urlopen', return_value=mock_response):
        json = fetch_store_json(LOOKUP_URL)

    assert '{"resultCount":12, "results": [{}]}' == json


def test_fetch_store_json_with_http_error():
    mock_response = MagicMock()
    mock_response.getcode.return_value = 500

    with patch('urllib.request.urlopen', return_value=mock_response):
        with pytest.raises(ApitError):
            fetch_store_json(LOOKUP_URL)


@pytest.mark.integration
def test_fetch_store_json_with_real_data_from_itunes():
    REAL_LOOKUP_URL = 'https://itunes.apple.com/lookup?entity=song&country=us&id=1440742903'

    json_str = fetch_store_json(REAL_LOOKUP_URL)

    data = json.loads(json_str)

    assert data['resultCount'] == 15

    # test some album data
    assert data['results'][0]['collectionId'] == 1440742903
    assert data['results'][0]['collectionType'] == 'Album'
    assert data['results'][0]['artistName'] == 'Kanye West'
    assert data['results'][0]['collectionName'] == 'My Beautiful Dark Twisted Fantasy'
    assert data['results'][0]['copyright'] == '℗ 2010 Roc-A-Fella Records, LLC'

    # test some song data
    assert data['results'][1]['kind'] == 'song'
    assert data['results'][1]['trackName'] == 'Dark Fantasy'
    assert data['results'][1]['trackNumber'] == 1
    assert data['results'][1]['trackCount'] == 13
