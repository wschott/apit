import pytest

from apit.cli import parse_args


def test_parse_args():
    args = parse_args(["show", "./tests/fixtures"])
    assert args.command == "show"
    assert args.path == "./tests/fixtures"
    assert not args.has_backup_flag
    assert not args.has_search_result_cache_flag


def test_parse_args_optional_args():
    args = parse_args(["-v", "show", "./tests/fixtures"])
    assert args.verbose_level == 1

    args = parse_args(["-vv", "show", "./tests/fixtures"])
    assert args.verbose_level == 2

    args = parse_args(["-b", "tag", "./tests/fixtures"])
    assert args.has_backup_flag

    args = parse_args(["-c", "tag", "./tests/fixtures"])
    assert args.has_search_result_cache_flag

    args = parse_args(["tag", "./tests/fixtures", "http://invalid-url.com/"])
    assert args.source == "http://invalid-url.com/"

    args = parse_args(["tag", "./tests/fixtures", "test-metadata-file.json"])
    assert args.source == "test-metadata-file.json"

    args = parse_args(["-a", "tag", "./tests/fixtures"])
    assert args.has_embed_artwork_flag
    assert args.artwork_size == 600

    args = parse_args(["--artwork-size", "700", "tag", "./tests/fixtures"])
    assert args.artwork_size == 700


def test_parse_args_complex_args(tmp_path):
    args = parse_args(
        ["--cache", "--backup", "-v", "tag", str(tmp_path), "test-metadata-file.json"]
    )
    assert args.has_search_result_cache_flag
    assert args.has_backup_flag
    assert args.verbose_level == 1
    assert args.command == "tag"
    assert args.path == str(tmp_path)
    assert args.source == "test-metadata-file.json"


def test_parse_args_missing_command():
    with pytest.raises(SystemExit):
        parse_args(["."])


def test_parse_args_missing_folder():
    with pytest.raises(SystemExit):
        parse_args(["show"])


def test_parse_args_invalid_option():
    with pytest.raises(SystemExit):
        parse_args(["-x", "show", "./tests/fixtures"])
