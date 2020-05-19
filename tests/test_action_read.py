from pathlib import Path

import pytest

from apit.commands.show.action import ReadAction
from apit.error import ApitError


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


def test_read_action_apply(monkeypatch):
    monkeypatch.setattr('apit.commands.show.action.read_metadata', lambda *args: 'mock-metadata')
    action = ReadAction(Path('./tests/fixtures/folder-iteration/1 first.m4a'), {})

    action.apply()

    assert action.result == 'mock-metadata'
    assert action.executed
    assert action.successful
    assert action.status_msg == 'successful'


def test_read_action_apply_error_while_reading(monkeypatch):
    def _raise(*args):
        raise ApitError()
    monkeypatch.setattr('apit.commands.show.action.read_metadata', _raise)
    action = ReadAction(Path('./tests/fixtures/folder-iteration/1 first.m4a'), {})

    action.apply()

    assert isinstance(action.result, ApitError)
    assert action.executed
    assert not action.successful
    assert action.status_msg == '[error]'
