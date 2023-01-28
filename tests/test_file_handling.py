from pathlib import Path

import pytest

from apit.file_handling import backup_file
from apit.file_handling import collect_files
from apit.file_handling import extract_disc_and_track_number


def test_collect_files_using_folder(tmp_path, make_tmp_file):
    file_1 = make_tmp_file("1 first.m4a")
    file_2 = make_tmp_file("2 second.mp3")
    file_3 = make_tmp_file("3 third.mp4")

    assert collect_files(tmp_path) == [file_1, file_2, file_3]


def test_collect_files_uses_natural_order_sorting(tmp_path, make_tmp_file):
    file_1 = make_tmp_file("1 first.m4a")
    file_27 = make_tmp_file("27 second.mp3")
    file_3 = make_tmp_file("3 third.mp4")

    assert collect_files(tmp_path) == [file_1, file_3, file_27]


def test_collect_files_using_single_file(make_tmp_file):
    file_1 = make_tmp_file("1 first.m4a")

    assert collect_files(file_1) == [file_1]


@pytest.mark.parametrize("filter_ext", ["m4a", ["m4a"]])
def test_collect_files_using_filter(filter_ext, tmp_path, make_tmp_file):
    file_1 = make_tmp_file("1 first.m4a")
    make_tmp_file("2 second.mp3")
    make_tmp_file("3 third.mp4")

    assert collect_files(tmp_path, filter_ext) == [file_1]


@pytest.mark.parametrize(
    "path",
    [
        "14.m4a",
        "14..m4a",
        "#14.m4a",
        "14 song title.m4a",
        "14song title.m4a",
        "14. song title.m4a",
        "14.song title.m4a",
        "#14 song title.m4a",
    ],
)
def test_extract_disc_and_track_number_using_only_track_number(path: str):
    assert extract_disc_and_track_number(Path(path)) == (1, 14)


@pytest.mark.parametrize(
    "path",
    [
        "2 14 song title.m4a",
        "2. 14 song title.m4a",
        "2. 14. song title.m4a",
    ],
)
def test_extract_disc_and_track_number_using_only_track_number_containing_numbers_in_title(
    path: str,
):
    assert extract_disc_and_track_number(Path(path)) == (1, 2)


@pytest.mark.parametrize(
    "path",
    [
        "2-14.m4a",
        "2.14.m4a",
        "2.14..m4a",
        "2.14..m4a",
        "#2-14.m4a",
        "2-14song title.m4a",
        "2-14 song title.m4a",
        "2.14 song title.m4a",
        "2.14.song title.m4a",
        "2-14.song title.m4a",
        "2.14. song title.m4a",
        "2-14. song title.m4a",
    ],
)
def test_extract_disc_and_track_number_using_disc_and_track_number(path: str):
    assert extract_disc_and_track_number(Path(path)) == (2, 14)


def test_extract_disc_and_track_number_using_invalid_filename():
    assert extract_disc_and_track_number(Path("song title.m4a")) == (None, None)


def test_backup_file(make_tmp_file):
    file = make_tmp_file("original.m4a")
    assert not file.with_name("original.bak.m4a").exists()

    backup_file(file)

    assert file.with_name("original.bak.m4a").exists()
