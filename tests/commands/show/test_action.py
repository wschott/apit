from pathlib import Path
from unittest.mock import MagicMock

from apit.commands.show.action import ReadAction
from apit.commands.show.reporting.file_tags import FileTags
from apit.commands.show.reporting.mp4.mp4_tag import Mp4Tag
from apit.error import ApitError
from apit.tag_id import TagId


def test_read_action_after_init():
    action = ReadAction(
        Path("./tests/fixtures/folder-iteration/1 first.m4a"), {"key": "test"}
    )

    assert action.file == Path("./tests/fixtures/folder-iteration/1 first.m4a")
    assert action.options == {"key": "test"}
    assert not action.executed
    assert not action.successful
    assert not action.needs_confirmation
    assert not action.result
    assert action.actionable


def test_read_action_apply(monkeypatch):
    monkeypatch.setattr(
        "apit.commands.show.action.read_metadata",
        lambda *args: MagicMock(tags={"tag_id": "tag_value"}),
    )
    action = ReadAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})

    action.apply()

    assert action.executed
    assert action.successful
    assert isinstance(action.result, FileTags)
    assert action.result._tags == [Mp4Tag(TagId("tag_id"), "tag_value")]


def test_read_action_apply_error_while_reading(monkeypatch):
    error = ApitError("mock-error")

    def _raise(*args):
        raise error

    monkeypatch.setattr("apit.commands.show.action.read_metadata", _raise)
    action = ReadAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})

    action.apply()

    assert action.executed
    assert not action.successful
    assert action.result == error
