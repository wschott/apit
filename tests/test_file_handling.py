from pathlib import Path

import pytest

from apit.error import ApitError
from apit.file_handling import collect_files, extract_disc_and_track_number


# TODO create temporary files for testing?
def test_collect_files():
    assert collect_files('tests/fixtures/folder-iteration') == [
        Path('tests/fixtures/folder-iteration/1 first.m4a'),
        Path('tests/fixtures/folder-iteration/2 second.mp3'),
        Path('tests/fixtures/folder-iteration/3 third.mp4')
    ]

def test_collect_files_using_filter():
    assert collect_files('tests/fixtures/folder-iteration', '.m4a') == [
        Path('tests/fixtures/folder-iteration/1 first.m4a')
    ]
    assert collect_files('tests/fixtures/folder-iteration', ['.m4a']) == [
        Path('tests/fixtures/folder-iteration/1 first.m4a')
    ]

def test_extract_disc_and_track_number_using_both_numbers():
    assert extract_disc_and_track_number(Path('2-14 song title.m4a')) == (2, 14)

def test_extract_disc_and_track_number_using_only_track_number():
    assert extract_disc_and_track_number(Path('14 song title.m4a')) == (1, 14)

def test_extract_disc_and_track_number_using_invalid_filename():
    with pytest.raises(ApitError):
        assert extract_disc_and_track_number(Path('song title.m4a')) == (1, 14)
