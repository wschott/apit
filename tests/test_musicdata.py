import pytest

from apit.error import ApitError
from apit.musicdata import (
    extract_album_and_song_data,
    fetch_store_json_string,
    generate_store_lookup_url,
)

STORE_URL = 'https://music.apple.com/us/album/test-album/12345'
STORE_URL_COMPLEX = 'http://test.com/us/test/42/12345?i=09876/54321'
STORE_URL_ANYTHING = 'http://x/us/x/9/12345?i=09876'
STORE_URL_OLD = 'http://itunes.apple.com/us/album/test-album/id12345'
LOOKUP_URL = 'https://itunes.apple.com/lookup?entity=song&country=us&id=12345'
REAL_LOOKUP_URL = 'https://itunes.apple.com/lookup?entity=song&country=us&id=1440742903'

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

def test_process_album(test_metadata):
    album = extract_album_and_song_data(test_metadata)

    assert album['collectionId'] == 1440742903
    assert album['artistName'] == 'Kanye West'
    assert album['collectionName'] == 'My Beautiful Dark Twisted Fantasy'

def test_process_songs(test_metadata):
    album = extract_album_and_song_data(test_metadata)

    song = album.getSong(3)
    assert song['kind'] == 'song'
    assert song['discNumber'] == 1
    assert song['trackNumber'] == 3
    assert song['trackName'] == 'Power'

def test_process_album_invalid_json():
    with pytest.raises(ApitError):
        extract_album_and_song_data('{"results":[], "resultCount": 0}')

@pytest.mark.integration
@pytest.mark.xfail
def test_real_fetching_of_data_from_itunes():
    json = fetch_store_json_string(REAL_LOOKUP_URL)
    print(json)
    assert b'{\n "resultCount":15,\n "results": [\n{' in json
    assert 0
