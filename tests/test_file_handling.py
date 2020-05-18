from pathlib import Path

import pytest

from apit.error import ApitError
from apit.file_handling import (
    MIME_TYPE,
    _generate_filename_prefix,
    collect_files,
    extract_disc_and_track_number,
    generate_artwork_filename,
    generate_cache_filename,
)


# TODO create temporary files for testing?
def test_collect_files_using_folder():
    assert collect_files(Path('tests/fixtures/folder-iteration')) == [
        Path('tests/fixtures/folder-iteration/1 first.m4a'),
        Path('tests/fixtures/folder-iteration/2 second.mp3'),
        Path('tests/fixtures/folder-iteration/3 third.mp4')
    ]


def test_collect_files_using_single_file():
    assert collect_files(Path('tests/fixtures/folder-iteration/1 first.m4a')) == [
        Path('tests/fixtures/folder-iteration/1 first.m4a'),
    ]


def test_collect_files_using_filter():
    assert collect_files(Path('tests/fixtures/folder-iteration'), '.m4a') == [
        Path('tests/fixtures/folder-iteration/1 first.m4a')
    ]
    assert collect_files(Path('tests/fixtures/folder-iteration'), ['.m4a']) == [
        Path('tests/fixtures/folder-iteration/1 first.m4a')
    ]


def test_collect_files_using_non_existing_folder():
    with pytest.raises(ApitError, match='Invalid path'):
        collect_files(Path('./non-existing'))


def test_extract_disc_and_track_number_using_only_track_number():
    assert extract_disc_and_track_number(Path('14.m4a')) == (1, 14)
    assert extract_disc_and_track_number(Path('14..m4a')) == (1, 14)
    assert extract_disc_and_track_number(Path('#14.m4a')) == (1, 14)
    assert extract_disc_and_track_number(Path('14 song title.m4a')) == (1, 14)
    assert extract_disc_and_track_number(Path('14song title.m4a')) == (1, 14)
    assert extract_disc_and_track_number(Path('14. song title.m4a')) == (1, 14)
    assert extract_disc_and_track_number(Path('14.song title.m4a')) == (1, 14)
    assert extract_disc_and_track_number(Path('#14 song title.m4a')) == (1, 14)


def test_extract_disc_and_track_number_using_only_track_number_containing_numbers_in_title():
    assert extract_disc_and_track_number(Path('2 14 song title.m4a')) == (1, 2)
    assert extract_disc_and_track_number(Path('2. 14 song title.m4a')) == (1, 2)
    assert extract_disc_and_track_number(Path('2. 14. song title.m4a')) == (1, 2)


def test_extract_disc_and_track_number_using_disc_and_track_number():
    assert extract_disc_and_track_number(Path('2-14.m4a')) == (2, 14)
    assert extract_disc_and_track_number(Path('2.14.m4a')) == (2, 14)
    assert extract_disc_and_track_number(Path('2.14..m4a')) == (2, 14)
    assert extract_disc_and_track_number(Path('2.14..m4a')) == (2, 14)
    assert extract_disc_and_track_number(Path('#2-14.m4a')) == (2, 14)
    assert extract_disc_and_track_number(Path('2-14song title.m4a')) == (2, 14)
    assert extract_disc_and_track_number(Path('2-14 song title.m4a')) == (2, 14)
    assert extract_disc_and_track_number(Path('2.14 song title.m4a')) == (2, 14)
    assert extract_disc_and_track_number(Path('2.14.song title.m4a')) == (2, 14)
    assert extract_disc_and_track_number(Path('2-14.song title.m4a')) == (2, 14)
    assert extract_disc_and_track_number(Path('2.14. song title.m4a')) == (2, 14)
    assert extract_disc_and_track_number(Path('2-14. song title.m4a')) == (2, 14)


def test_extract_disc_and_track_number_using_invalid_filename():
    assert not extract_disc_and_track_number(Path('song title.m4a'))


def test_generate_cache_filename(test_song):
    assert generate_cache_filename(Path('.'), test_song) == Path('./Album_Artist-Test_Album_Namè-12345.json')


def test_generate_artwork_filename(test_song):
    assert generate_artwork_filename(Path('.'), test_song, MIME_TYPE.JPEG) == Path('./Album_Artist-Test_Album_Namè-12345.jpg')
    assert generate_artwork_filename(Path('.'), test_song, MIME_TYPE.PNG) == Path('./Album_Artist-Test_Album_Namè-12345.png')


def test_generate_filename_prefix(test_song):
    assert _generate_filename_prefix(test_song) == 'Album_Artist-Test_Album_Namè-12345'
