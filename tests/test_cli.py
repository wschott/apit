from pathlib import Path

import pytest

from apit.cli import parse_args


def test_list_command():
    args = parse_args(["list", "./tests/fixtures"])
    assert args.command == "list"
    assert args.path == Path("./tests/fixtures").absolute()


def test_list_alias():
    args = parse_args(["ls", "./tests/fixtures"])
    assert args.command == "ls"


def test_tag_command():
    args = parse_args(["tag", "./tests/fixtures", "http://invalid-url.com/"])
    assert args.command == "tag"
    assert args.path == Path("./tests/fixtures").absolute()
    assert args.has_embed_artwork_flag
    assert args.artwork_size == 600


def test_tag_command_source_types():
    args = parse_args(["tag", "./tests/fixtures", "http://invalid-url.com/"])
    assert args.source == "http://invalid-url.com/"

    args = parse_args(["tag", "./tests/fixtures", "test-metadata-file.json"])
    assert args.source == "test-metadata-file.json"


def test_parse_args_optional_args():
    args = parse_args(["list", "-v", "./tests/fixtures"])
    assert args.verbose_level == 1

    args = parse_args(["list", "-vv", "./tests/fixtures"])
    assert args.verbose_level == 2

    args = parse_args(["tag", "-b", "./tests/fixtures", "./tests/metadata.json"])
    assert args.has_backup_flag

    args = parse_args(
        ["tag", "--no-artwork", "./tests/fixtures", "./tests/metadata.json"]
    )
    assert not args.has_embed_artwork_flag

    args = parse_args(
        ["tag", "--artwork-size", "700", "./tests/fixtures", "./tests/metadata.json"]
    )
    assert args.artwork_size == 700


def test_parse_args_complex_args(tmp_path):
    args = parse_args(
        ["tag", "--backup", "-v", str(tmp_path), "test-metadata-file.json"]
    )
    assert args.has_backup_flag
    assert args.verbose_level == 1
    assert args.command == "tag"
    assert args.path == tmp_path
    assert args.source == "test-metadata-file.json"


def test_parse_args_missing_command():
    with pytest.raises(SystemExit):
        parse_args(["."])


def test_parse_args_missing_folder():
    with pytest.raises(SystemExit):
        parse_args(["list"])


def test_parse_args_invalid_option():
    with pytest.raises(SystemExit):
        parse_args(["-x", "list", "./tests/fixtures"])


def test_parse_args_using_non_existing_folder():
    with pytest.raises(SystemExit):
        parse_args(["list", "./non-existing"])
