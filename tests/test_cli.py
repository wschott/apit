from argparse import ArgumentTypeError
from pathlib import Path

import pytest

from apit.cli import _to_path, parse_args


def test_parse_args():
    args = parse_args(['show', './tests/fixtures'])
    assert args.command == 'show'
    assert args.path == Path('./tests/fixtures')
    assert args.has_overwrite_flag
    assert not args.has_search_result_cache_flag


def test_parse_args_optional_args():
    args = parse_args(['-v', 'show', './tests/fixtures'])
    assert args.verbose_level == 1

    args = parse_args(['-vv', 'show', './tests/fixtures'])
    assert args.verbose_level == 2

    args = parse_args(['-t', 'tag', './tests/fixtures'])
    assert not args.has_overwrite_flag

    args = parse_args(['-c', 'tag', './tests/fixtures'])
    assert args.has_search_result_cache_flag

    args = parse_args(['tag', './tests/fixtures', 'http://invalid-url.com/'])
    assert args.source == 'http://invalid-url.com/'

    args = parse_args(['tag', './tests/fixtures', 'test-metadata-file.json'])
    assert args.source == 'test-metadata-file.json'


def test_parse_args_complex_args(tmp_path):
    args = parse_args(['--cache', '--temp', '-v', 'tag', str(tmp_path), 'test-metadata-file.json'])
    assert args.has_search_result_cache_flag
    assert not args.has_overwrite_flag
    assert args.verbose_level == 1
    assert args.command == 'tag'
    assert args.path == tmp_path
    assert args.source == 'test-metadata-file.json'


def test_parse_args_missing_command():
    with pytest.raises(SystemExit):
        parse_args(['.'])


def test_parse_args_missing_folder():
    with pytest.raises(SystemExit):
        parse_args(['show'])


def test_parse_args_invalid_folder():
    with pytest.raises(SystemExit):
        parse_args(['show', './non-existing-folder'])


def test_parse_args_invalid_option():
    with pytest.raises(SystemExit):
        parse_args(['-x', 'show', './tests/fixtures'])


def test_to_path_using_folder(tmp_path):
    # TODO test expanddir()
    assert _to_path('.') == Path('.')
    assert _to_path(str(tmp_path)) == tmp_path


def test_to_path_using_single_file():
    assert _to_path('tests/fixtures/folder-iteration/1 first.m4a') == Path('tests/fixtures/folder-iteration/1 first.m4a')


def test_to_path_invalid_folder():
    with pytest.raises(ArgumentTypeError):
        _to_path('./non-existing-folder')
