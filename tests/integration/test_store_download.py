import json
from pathlib import Path

import pytest

from apit.metadata_cache import save_to_cache
from apit.store.connection import fetch_store_json


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


@pytest.mark.integration
def test_downloaded_store_json_is_saved_using_unicode_chars(tmp_path, test_album):
    REAL_LOOKUP_URL = 'https://itunes.apple.com/lookup?entity=song&country=us&id=1440742903'

    json_str = fetch_store_json(REAL_LOOKUP_URL)
    save_to_cache(json_str, tmp_path, test_album)

    with Path(tmp_path / 'Test_Artist-Test_Collection-12345.json') as json_file:
        data_read = json_file.read_text()
    assert data_read == json_str

    data = json.loads(data_read)
    assert data['results'][0]['copyright'] == '℗ 2010 Roc-A-Fella Records, LLC'
