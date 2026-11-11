import pytest

from apit.file_handling import collect_files


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
