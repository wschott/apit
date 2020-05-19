from collections import namedtuple
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

from apit.atomic_parser import is_itunes_bought_file, read_metadata
from apit.error import ApitError

MockCompletedprocess = namedtuple('MockCompletedprocess', ['returncode', 'stdout', 'stderr', 'args'])

EXPECTED_SHOW_COMMAND = ['/Mock/AtomicParsley', 'dummy.m4a', '-t']


def test_is_itunes_bought_file(monkeypatch):
    monkeypatch.setattr('apit.atomic_parser.read_metadata', lambda *args: 'Atom "ownr" contains')
    assert is_itunes_bought_file(Path('tests/fixtures/1 itunes file.m4a'))


def test_is_itunes_bought_file_not_itunes_file(monkeypatch):
    monkeypatch.setattr('apit.atomic_parser.read_metadata', lambda *args: 'Atom "dummy" contains')
    assert not is_itunes_bought_file(Path('tests/fixtures/1 itunes file.m4a'))


def test_is_itunes_bought_file_file_error(monkeypatch):
    def _raise(*args):
        raise ApitError()
    monkeypatch.setattr('apit.atomic_parser.read_metadata', _raise)
    assert not is_itunes_bought_file(Path('tests/fixtures/1 itunes file.m4a'))


@patch('apit.cmd._run_subprocess')
def test_metadata_reading(mock_run_subprocess, mock_atomicparsley_exe):
    mock_run_subprocess.return_value = MockCompletedprocess(0, 'mock-metadata', '', '')

    result = read_metadata(Path('dummy.m4a'))

    assert mock_run_subprocess.call_args == call(EXPECTED_SHOW_COMMAND, shell=False)
    assert result == 'mock-metadata'


@patch('apit.cmd._run_subprocess')
def test_metadata_reading_error(mock_run_subprocess, mock_atomicparsley_exe):
    mock_run_subprocess.return_value = MockCompletedprocess(1, '', 'mock-error', '')

    with pytest.raises(ApitError, match='mock-error'):
        read_metadata(Path('dummy.m4a'))

    assert mock_run_subprocess.call_args == call(EXPECTED_SHOW_COMMAND, shell=False)
