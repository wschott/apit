from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from apit.actions import ReadAction


def test_read_action_to_action_options():
    assert ReadAction.to_action_options({}) == {}
    assert ReadAction.to_action_options({'key': 'value'}) == {}


def test_read_action_after_init():
    action = ReadAction(Path('./tests/fixtures/folder-iteration/1 first.m4a'), {'key': 'test'})

    assert action.file == Path('./tests/fixtures/folder-iteration/1 first.m4a')
    assert action.options == {'key': 'test'}
    assert not action.executed
    assert not action.successful
    assert not action.needs_confirmation
    assert action.actionable
    assert action.preview_msg == ''
    assert action.status_msg == '[error]'
    with pytest.raises(NotImplementedError):
        action.not_actionable_msg


@patch('apit.cmd._run_subprocess')
def test_read_action_apply(mock_run_subprocess, mock_atomicparsley_exe):
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_run_subprocess.return_value = mock_result
    action = ReadAction(Path('./tests/fixtures/folder-iteration/1 first.m4a'), {})

    action.apply()

    assert action.result == mock_result
    assert action.result.returncode == 0
    assert action.executed
    assert action.successful
    assert action.status_msg == 'successful'


@patch('apit.cmd._run_subprocess')
def test_read_action_apply_error_while_reading(mock_run_subprocess, mock_atomicparsley_exe):
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_run_subprocess.return_value = mock_result
    action = ReadAction(Path('./tests/fixtures/folder-iteration/1 first.m4a'), {})

    action.apply()

    assert action.result == mock_result
    assert action.result.returncode == 1
    assert action.executed
    assert not action.successful
    assert action.status_msg == '[error]'
