from pathlib import Path
from unittest.mock import call, patch

import pytest

from apit.cmd import (
    _create_shell_friendly_filename,
    _escape_shell_arguments,
    _find_atomicparsley_executable,
    _generate_shell_command,
    _to_list,
    execute_command,
)
from apit.error import ApitError


def test_to_list():
    assert _to_list('test1') == ['test1']
    assert _to_list(['test2']) == ['test2']


def test_shell_argument_escaping():
    assert _escape_shell_arguments('test test') == 'test test'
    assert _escape_shell_arguments('test &test') == 'test &test'
    assert _escape_shell_arguments('test (test)') == 'test (test)'
    assert _escape_shell_arguments('test $ test') == 'test \\$ test'
    assert _escape_shell_arguments('test `test`') == 'test \\`test\\`'
    assert _escape_shell_arguments('--artist "foobar"') == '--artist "foobar"'
    assert _escape_shell_arguments('--artist "foo "bar" baz"') == '--artist "foo \\"bar\\" baz"'
    assert _escape_shell_arguments('--artist "foo "bar" baz" test') == '--artist "foo \\"bar\\" baz" test'


def test_shell_friendly_filename_creation():
    assert _create_shell_friendly_filename('dummy.m4a') == '"dummy.m4a"'


def test_shell_command_generation_containing_unicode():
    assert _generate_shell_command('/Mock/AtomicParsley', 'dummy.m4a', ['--artist "Namé"'], shell=True) == '/Mock/AtomicParsley "dummy.m4a" --artist "Namé"'


def test_shell_command_generation_containing_chars_to_escape():
    assert _generate_shell_command('/Mock/AtomicParsley', 'dummy.m4a', ['a', '--b "foo $bar"'], shell=True) == '/Mock/AtomicParsley "dummy.m4a" a --b "foo \\$bar"'


@patch('apit.cmd._run_subprocess')
def test_command_execution_not_shell(mock_run_subprocess, mock_atomicparsley_exe):
    _ = execute_command('dummy.m4a', '--my-test "test"')
    assert mock_run_subprocess.call_args == call(['/Mock/AtomicParsley', 'dummy.m4a', '--my-test "test"'], shell=False)


@patch('apit.cmd._run_subprocess')
def test_command_execution_for_shell(mock_run_subprocess, mock_atomicparsley_exe):
    _ = execute_command('dummy.m4a', '--my-test "test"', shell=True)
    assert mock_run_subprocess.call_args == call('/Mock/AtomicParsley "dummy.m4a" --my-test "test"', shell=True)


def test_atomicparsley_finding(mock_atomicparsley_exe):
    assert _find_atomicparsley_executable([
        'tests/non-existing/AtomicParsley',
        'tests/fixtures/AtomicParsley',
    ]) == Path('tests/fixtures/AtomicParsley')


def test_atomicparsley_finding_no_exe():
    with pytest.raises(ApitError, match='executable not found'):
        _find_atomicparsley_executable([])


@pytest.fixture
def mock_atomicparsley_exe_missing(monkeypatch):
    def _raise(*args):
        raise ApitError('TestParsley not found')

    monkeypatch.setattr('apit.cmd._find_atomicparsley_executable', _raise)


def test_execute(mock_atomicparsley_exe_missing):
    with pytest.raises(ApitError, match='TestParsley'):
        execute_command('dummy.m4a', '-t')
