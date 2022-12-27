from pathlib import Path
from unittest.mock import call
from unittest.mock import MagicMock

from apit.commands.show.action import ReadAction
from apit.error import ApitError


def test_read_action_after_init():
    action = ReadAction(
        Path("./tests/fixtures/folder-iteration/1 first.m4a"), {"key": "test"}
    )

    assert action.file == Path("./tests/fixtures/folder-iteration/1 first.m4a")
    assert action.options == {"key": "test"}
    assert not action.executed
    assert not action.successful
    assert not action.needs_confirmation
    assert action.actionable


def test_read_action_apply(monkeypatch):
    mp4_mock = MagicMock(tags="mock_metadata")
    monkeypatch.setattr(
        "apit.commands.show.action.read_metadata", lambda *args: mp4_mock
    )
    action = ReadAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})
    mock_mark_as_success = MagicMock()
    monkeypatch.setattr(action, "mark_as_success", mock_mark_as_success)

    action.apply()

    assert mock_mark_as_success.call_args == call(mp4_mock)


def test_read_action_apply_error_while_reading(monkeypatch):
    error = ApitError("mock-error")

    def _raise(*args):
        raise error

    monkeypatch.setattr("apit.commands.show.action.read_metadata", _raise)
    action = ReadAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})
    mock_mark_as_fail = MagicMock()
    monkeypatch.setattr(action, "mark_as_fail", mock_mark_as_fail)

    action.apply()

    assert mock_mark_as_fail.call_args == call(error)
