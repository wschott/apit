from unittest.mock import MagicMock

from apit.commands.tag.action import TagAction
from apit.error import ApitError
from apit.file_tags import FileTags
from apit.metadata import Song


def test_tag_action_after_init(make_tmp_file, test_song: Song):
    tmp_file = make_tmp_file("2-3 first.m4a")

    action = TagAction(
        file=tmp_file,
        song=test_song,
        should_backup=False,
        artwork=None,
    )

    assert action.file == tmp_file
    assert action.song == test_song
    assert action.disc == test_song.disc_number
    assert action.track == test_song.track_number
    assert action.should_backup is False
    assert action.artwork is None
    assert not action.executed
    assert not action.successful
    assert action.needs_confirmation

    assert action.file_matched
    assert action.metadata_matched
    assert action.song == test_song
    assert action.actionable


def test_tag_action_file_matched(make_tmp_file):
    # TODO improve test: match against song
    action = TagAction(
        file=make_tmp_file("1 first.m4a"),
        song=None,
        should_backup=False,
        artwork=None,
    )

    assert action.file_matched


def test_tag_action_file_not_matched(make_tmp_file):
    # TODO improve test: match against song
    action = TagAction(
        file=make_tmp_file("first.m4a"),
        song=None,
        should_backup=False,
        artwork=None,
    )

    assert not action.file_matched


def test_tag_action_metadata_matched(make_tmp_file, test_song: Song):
    action = TagAction(
        file=make_tmp_file("1 first.m4a"),
        song=test_song,
        should_backup=False,
        artwork=None,
    )

    assert action.metadata_matched
    assert action.song == test_song


def test_tag_action_metadata_not_matched(make_tmp_file):
    action = TagAction(
        file=make_tmp_file("1 first.m4a"),
        song=None,
        should_backup=False,
        artwork=None,
    )

    assert not action.metadata_matched
    assert action.song is None


def test_tag_action_is_filename_identical_to_song(make_tmp_file, test_song: Song):
    action = TagAction(
        file=make_tmp_file("2-3 Track (feat. Other & $Artist) [Bonus Track].m4a"),
        song=test_song,
        should_backup=False,
        artwork=None,
    )

    assert action.is_filename_identical_to_song


def test_tag_action_not_is_filename_identical_to_song(make_tmp_file, test_song: Song):
    action = TagAction(
        file=make_tmp_file("2-3 any unknown song name.m4a"),
        song=test_song,
        should_backup=False,
        artwork=None,
    )

    assert not action.is_filename_identical_to_song


def test_tag_action_is_filename_with_strange_chars_identical_to_song(
    make_tmp_file, test_song: Song
):
    action = TagAction(
        file=make_tmp_file("2-3 Track! feat.=; [Other & $Artist]_Bonus Track-.m4a"),
        song=test_song,
        should_backup=False,
        artwork=None,
    )

    assert action.is_filename_identical_to_song


def test_tag_action_actionable(make_tmp_file, test_song: Song):
    action = TagAction(
        file=make_tmp_file("2-3 first.m4a"),
        song=test_song,
        should_backup=False,
        artwork=None,
    )

    assert action.actionable


def test_tag_action_not_actionable_due_to_missing_file(make_tmp_file, test_song: Song):
    action = TagAction(
        file=make_tmp_file("first.m4a"),
        song=test_song,
        should_backup=False,
        artwork=None,
    )

    assert not action.actionable


def test_tag_action_not_actionable_due_to_missing_metadata(
    make_tmp_file, test_song: Song
):
    action = TagAction(
        file=make_tmp_file("2-3 first.m4a"),
        song=None,
        should_backup=False,
        artwork=None,
    )

    assert not action.actionable


def test_tag_action_needs_confirmation(make_tmp_file, test_song: Song):
    action = TagAction(
        file=make_tmp_file("2-3 first.m4a"),
        song=test_song,
        should_backup=False,
        artwork=None,
    )

    assert action.needs_confirmation


def test_tag_action_needs_confirmation_false(make_tmp_file):
    action = TagAction(
        file=make_tmp_file("first.m4a"),
        song=None,
        should_backup=False,
        artwork=None,
    )

    assert not action.needs_confirmation


def test_tag_action_apply_not_actionable(monkeypatch, make_tmp_file):
    action = TagAction(
        file=make_tmp_file("first.m4a"),
        song=None,
        should_backup=False,
        artwork=None,
    )

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
    monkeypatch.setattr("apit.file_type.mp4.update_metadata", lambda *args: MagicMock())
    monkeypatch.setattr("apit.file_type.mp4.to_file_tags", lambda *args: test_file_tags)

    action = TagAction(
        file=make_tmp_file("2-3 first.m4a"),
        song=test_song,
        should_backup=False,
        artwork=None,
    )

    action.apply()

    assert action.executed
    assert action.successful
    assert action.result == test_file_tags


def test_tag_action_apply_error(monkeypatch, make_tmp_file, test_song: Song):
    error = ApitError("mock-error")

    def _raise(*args):
        raise error

    monkeypatch.setattr("apit.file_type.mp4.update_metadata", _raise)

    action = TagAction(
        file=make_tmp_file("2-3 first.m4a"),
        song=test_song,
        should_backup=False,
        artwork=None,
    )

    action.apply()

    assert action.executed
    assert not action.successful
    assert action.result == error
