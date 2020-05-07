from apit.metadata_store import _generate_log_filename, save_log
from apit.musicdata import extract_album_and_song_data

EXPECTED_FILENAME = 'Kanye_West-My_Beautiful_Dark_Twisted_Fantasy-1440742903.json'

def test_log_filename_generation(test_metadata):
    album = extract_album_and_song_data(test_metadata)
    assert _generate_log_filename(album) == EXPECTED_FILENAME

def test_log_file_creation(tmp_path, test_metadata):
    save_log(test_metadata, tmp_path)

    expected_logfile_path = (tmp_path / EXPECTED_FILENAME)
    assert expected_logfile_path.exists()

    assert expected_logfile_path.read_text() == test_metadata
