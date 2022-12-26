import json
import subprocess

import pytest

from apit.cache import save_artwork_to_cache, save_metadata_to_cache
from apit.store.connection import download_artwork, download_metadata

REAL_LOOKUP_URL = 'https://itunes.apple.com/lookup?entity=song&country=us&id=1440742903'
REAL_ARTWORK_URL = 'https://is1-ssl.mzstatic.com/image/thumb/Music128/v4/88/92/4c/88924c01-6fb3-8616-f0b3-881b1ed09e03/source/100x100bb.jpg'


@pytest.mark.integration
def test_download_metadata_using_real_itunes_data():
    json_str = download_metadata(REAL_LOOKUP_URL)

    data = json.loads(json_str)

    assert data['resultCount'] == 15

    # test some album data
    assert data['results'][0]['collectionId'] == 1440742903
    assert data['results'][0]['collectionType'] == 'Album'
    assert data['results'][0]['artistName'] == 'Kanye West'
    assert data['results'][0]['collectionName'] == 'My Beautiful Dark Twisted Fantasy'
    assert data['results'][0]['copyright'] == '℗ 2010 UMG Recordings, Inc.'

    # test some song data
    assert data['results'][1]['kind'] == 'song'
    assert data['results'][1]['trackName'] == 'Dark Fantasy'
    assert data['results'][1]['trackNumber'] == 1
    assert data['results'][1]['trackCount'] == 13


@pytest.mark.integration
def test_downloaded_metadata_json_is_saved_using_unicode_chars(tmp_path):
    cache_file = tmp_path / 'test-file.json'

    json_str = download_metadata(REAL_LOOKUP_URL)
    save_metadata_to_cache(json_str, cache_file)

    data_read = cache_file.read_text()
    assert data_read == json_str
    data = json.loads(data_read)
    assert data['results'][0]['copyright'] == '℗ 2010 UMG Recordings, Inc.'


@pytest.mark.integration
def test_downloaded_artwork(tmp_path):
    cache_file = tmp_path / 'test-file.jpg'

    artwork_content, image_type = download_artwork(REAL_ARTWORK_URL)
    save_artwork_to_cache(artwork_content, cache_file)

    data_read = cache_file.read_bytes()
    assert data_read == artwork_content
    assert b'JFIF' in data_read
    assert 'JPEG image data' in subprocess.run(['file', cache_file], text=True, capture_output=True).stdout
