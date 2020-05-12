from apit.metadata_cache import _generate_cache_filename, save_to_cache

EXPECTED_FILENAME = 'Test_Artist-Test_Collection-12345.json'


def test_cache_filename_generation(test_album):
    assert _generate_cache_filename(test_album) == EXPECTED_FILENAME


def test_cache_file_creation(tmp_path, test_metadata, test_album):
    expected_logfile_path = tmp_path / EXPECTED_FILENAME
    assert not expected_logfile_path.exists()

    save_to_cache(test_metadata, tmp_path, test_album)

    assert expected_logfile_path.exists()
    assert expected_logfile_path.read_text() == test_metadata


def test_cache_file_creation_creates_folder_hierarchy(tmp_path, test_metadata, test_album):
    sub_path = tmp_path / 'test-folder'
    expected_logfile_path = sub_path / EXPECTED_FILENAME
    assert not expected_logfile_path.exists()

    save_to_cache(test_metadata, sub_path, test_album)

    assert expected_logfile_path.exists()
    assert expected_logfile_path.read_text() == test_metadata
