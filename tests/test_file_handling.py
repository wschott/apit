from pathlib import Path

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


def test_collect_files_using_filter(tmp_path, make_tmp_file):
    file_1 = make_tmp_file("1 first.m4a")
    make_tmp_file("2 second.mp3")
    make_tmp_file("3 third.mp4")

    assert collect_files(tmp_path, "m4a") == [file_1]
    assert collect_files(tmp_path, ["m4a"]) == [file_1]


def test_extract_disc_and_track_number_using_only_track_number():
    assert extract_disc_and_track_number(Path("14.m4a")) == (1, 14)
    assert extract_disc_and_track_number(Path("14..m4a")) == (1, 14)
    assert extract_disc_and_track_number(Path("#14.m4a")) == (1, 14)
    assert extract_disc_and_track_number(Path("14 song title.m4a")) == (1, 14)
    assert extract_disc_and_track_number(Path("14song title.m4a")) == (1, 14)
    assert extract_disc_and_track_number(Path("14. song title.m4a")) == (1, 14)
    assert extract_disc_and_track_number(Path("14.song title.m4a")) == (1, 14)
    assert extract_disc_and_track_number(Path("#14 song title.m4a")) == (1, 14)


def test_extract_disc_and_track_number_using_only_track_number_containing_numbers_in_title():
    assert extract_disc_and_track_number(Path("2 14 song title.m4a")) == (1, 2)
    assert extract_disc_and_track_number(Path("2. 14 song title.m4a")) == (1, 2)
    assert extract_disc_and_track_number(Path("2. 14. song title.m4a")) == (1, 2)


def test_extract_disc_and_track_number_using_disc_and_track_number():
    assert extract_disc_and_track_number(Path("2-14.m4a")) == (2, 14)
    assert extract_disc_and_track_number(Path("2.14.m4a")) == (2, 14)
    assert extract_disc_and_track_number(Path("2.14..m4a")) == (2, 14)
    assert extract_disc_and_track_number(Path("2.14..m4a")) == (2, 14)
    assert extract_disc_and_track_number(Path("#2-14.m4a")) == (2, 14)
    assert extract_disc_and_track_number(Path("2-14song title.m4a")) == (2, 14)
    assert extract_disc_and_track_number(Path("2-14 song title.m4a")) == (2, 14)
    assert extract_disc_and_track_number(Path("2.14 song title.m4a")) == (2, 14)
    assert extract_disc_and_track_number(Path("2.14.song title.m4a")) == (2, 14)
    assert extract_disc_and_track_number(Path("2-14.song title.m4a")) == (2, 14)
    assert extract_disc_and_track_number(Path("2.14. song title.m4a")) == (2, 14)
    assert extract_disc_and_track_number(Path("2-14. song title.m4a")) == (2, 14)


def test_extract_disc_and_track_number_using_invalid_filename():
    assert extract_disc_and_track_number(Path("song title.m4a")) == (None, None)
