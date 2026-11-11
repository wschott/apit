from unittest.mock import MagicMock

from apit.core.audio.file_tags import FileTags
from apit.core.errors import ApitError
from apit.core.metadata.song import Song
from tests.conftest import FakeFile
from tests.conftest import make_tag_action


def test_tag_action_after_init(make_tmp_file, test_song: Song):
    tmp_file = make_tmp_file("2-3 first.m4a")

    action = make_tag_action(tmp_file, test_song)

    assert action.file == tmp_file
    assert action.match.song == test_song
    assert action.should_backup is False
    assert action.artwork is None
    assert not action.executed
    assert not action.successful
    assert action.needs_confirmation
    assert action.actionable


def test_tag_action_actionable(make_tmp_file, test_song: Song):
    action = make_tag_action(make_tmp_file("2-3 first.m4a"), test_song)

    assert action.actionable


def test_tag_action_not_actionable_due_to_missing_file(make_tmp_file, test_song: Song):
    action = make_tag_action(make_tmp_file("first.m4a"), test_song)

    assert not action.actionable


def test_tag_action_not_actionable_due_to_missing_metadata(make_tmp_file):
    action = make_tag_action(make_tmp_file("2-3 first.m4a"))

    assert not action.actionable


def test_tag_action_needs_confirmation(make_tmp_file, test_song: Song):
    action = make_tag_action(make_tmp_file("2-3 first.m4a"), test_song)

    assert action.needs_confirmation


def test_tag_action_needs_confirmation_false(make_tmp_file):
    action = make_tag_action(make_tmp_file("first.m4a"))

    assert not action.needs_confirmation


def test_tag_action_apply_not_actionable(monkeypatch, make_tmp_file):
    action = make_tag_action(make_tmp_file("first.m4a"))

    mock_mark_as_success = MagicMock()
    monkeypatch.setattr(action, "mark_as_success", mock_mark_as_success)
    mock_mark_as_fail = MagicMock()
    monkeypatch.setattr(action, "mark_as_fail", mock_mark_as_fail)

    assert not action.executed

    action.apply()

    assert not action.executed
    assert mock_mark_as_fail.call_args is None
    assert mock_mark_as_success.call_args is None


def test_tag_action_apply(
    monkeypatch, make_tmp_file, test_song: Song, test_file_tags: FileTags
):
    monkeypatch.setattr("apit.file_types.file_types", {"fake": FakeFile})
    action = make_tag_action(make_tmp_file("2-3 first.fake"), test_song)

    action.apply()

    assert action.executed
    assert action.successful
    assert action.result == test_file_tags


def test_tag_action_apply_error(monkeypatch, make_tmp_file, test_song: Song):
    error = ApitError("mock-error")

    def _raise(*args):
        raise error

    monkeypatch.setattr("apit.file_types.file_types", {"fake": _raise})
    action = make_tag_action(make_tmp_file("2-3 first.fake"), test_song)

    action.apply()

    assert action.executed
    assert not action.successful
    assert action.result == error
