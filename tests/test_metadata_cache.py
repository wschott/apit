from apit.cache import save_metadata_to_cache


def test_cache_file_creation(tmp_path, test_metadata):
    cache_file = tmp_path / 'test-file.json'
    assert not cache_file.exists()

    save_metadata_to_cache(test_metadata, cache_file)

    assert cache_file.exists()
    assert cache_file.read_text() == test_metadata


def test_cache_file_creation_creates_folder_hierarchy(tmp_path, test_metadata):
    cache_file = tmp_path / 'test-folder/test-file.json'
    assert not cache_file.exists()

    save_metadata_to_cache(test_metadata, cache_file)

    assert cache_file.exists()
    assert cache_file.read_text() == test_metadata
