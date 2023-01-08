from pathlib import Path
from unittest.mock import MagicMock

from apit.commands.tag.action import TagAction
from apit.error import ApitError
from apit.file_tags import FileTags
from apit.metadata import Song
from apit.tag_id import TagId
from apit.tagging.mp4.mp4_tag import Mp4Tag


def test_tag_action_after_init(test_song: Song):
    action = TagAction(
        Path("./tests/fixtures/folder-iteration/1 first.m4a"),
        {
            "song": test_song,
            "disc": test_song.disc_number,
            "track": test_song.track_number,
            "is_original": False,
            "should_backup": False,
            "cover_path": None,
        },
    )

    assert action.file == Path("./tests/fixtures/folder-iteration/1 first.m4a")
    assert action.options == {
        "song": test_song,
        "disc": test_song.disc_number,
        "track": test_song.track_number,
        "is_original": False,
        "should_backup": False,
        "cover_path": None,
    }
    assert not action.executed
    assert not action.successful
    assert action.needs_confirmation

    assert action.file_matched
    assert action.metadata_matched
    assert action.song == test_song
    assert action.actionable


def test_tag_action_file_matched(monkeypatch, test_song: Song):
    action = TagAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})

    monkeypatch.setitem(action.options, "disc", test_song.disc_number)
    monkeypatch.setitem(action.options, "track", test_song.track_number)

    assert action.file_matched


def test_tag_action_file_not_matched(monkeypatch):
    action = TagAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})

    monkeypatch.setitem(action.options, "disc", None)
    monkeypatch.setitem(action.options, "track", 1)

    assert not action.file_matched

    monkeypatch.setitem(action.options, "disc", 1)
    monkeypatch.setitem(action.options, "track", None)

    assert not action.file_matched


def test_tag_action_metadata_matched(monkeypatch, test_song: Song):
    action = TagAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})

    monkeypatch.setitem(action.options, "song", test_song)

    assert action.metadata_matched
    assert action.song == test_song


def test_tag_action_metadata_not_matched(monkeypatch):
    action = TagAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})

    monkeypatch.setitem(action.options, "song", None)

    assert not action.metadata_matched
    assert action.song is None


def test_tag_action_is_filename_identical_to_song(monkeypatch, test_song: Song):
    action = TagAction(
        Path(
            "./tests/fixtures/folder-iteration/2-3 Track (feat. Other & $Artist) [Bonus Track].m4a"  # noqa: B950
        ),
        {},
    )

    monkeypatch.setitem(action.options, "song", test_song)
    monkeypatch.setitem(action.options, "disc", test_song.disc_number)
    monkeypatch.setitem(action.options, "track", test_song.track_number)
    monkeypatch.setitem(action.options, "is_original", False)

    assert action.is_filename_identical_to_song


def test_tag_action_not_is_filename_identical_to_song(monkeypatch, test_song: Song):
    action = TagAction(
        Path("./tests/fixtures/folder-iteration/1 any unknown song name.m4a"), {}
    )

    monkeypatch.setitem(action.options, "song", test_song)
    monkeypatch.setitem(action.options, "disc", test_song.disc_number)
    monkeypatch.setitem(action.options, "track", test_song.track_number)
    monkeypatch.setitem(action.options, "is_original", False)

    assert not action.is_filename_identical_to_song


def test_tag_action_actionable(monkeypatch, test_song):
    action = TagAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})

    monkeypatch.setitem(action.options, "song", test_song)
    monkeypatch.setitem(action.options, "disc", test_song.disc_number)
    monkeypatch.setitem(action.options, "track", test_song.track_number)
    monkeypatch.setitem(action.options, "is_original", False)

    assert action.actionable


def test_tag_action_not_actionable_due_to_missing_file(monkeypatch, test_song: Song):
    action = TagAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})

    monkeypatch.setitem(action.options, "song", test_song)
    monkeypatch.setitem(action.options, "disc", None)
    monkeypatch.setitem(action.options, "track", None)
    monkeypatch.setitem(action.options, "is_original", False)

    assert not action.actionable


def test_tag_action_not_actionable_due_to_missing_metadata(
    monkeypatch, test_song: Song
):
    action = TagAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})

    monkeypatch.setitem(action.options, "song", None)
    monkeypatch.setitem(action.options, "disc", test_song.disc_number)
    monkeypatch.setitem(action.options, "track", test_song.track_number)
    monkeypatch.setitem(action.options, "is_original", False)

    assert not action.actionable


def test_tag_action_not_actionable_due_to_itunes_original(monkeypatch, test_song: Song):
    action = TagAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})

    monkeypatch.setitem(action.options, "song", test_song)
    monkeypatch.setitem(action.options, "disc", test_song.disc_number)
    monkeypatch.setitem(action.options, "track", test_song.track_number)
    monkeypatch.setitem(action.options, "is_original", True)

    assert not action.actionable


def test_tag_action_needs_confirmation(monkeypatch, test_song: Song):
    action = TagAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})

    monkeypatch.setitem(action.options, "song", test_song)
    monkeypatch.setitem(action.options, "disc", test_song.disc_number)
    monkeypatch.setitem(action.options, "track", test_song.track_number)
    monkeypatch.setitem(action.options, "is_original", False)

    assert action.needs_confirmation


def test_tag_action_needs_confirmation_false(monkeypatch):
    action = TagAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})

    monkeypatch.setitem(action.options, "song", None)
    monkeypatch.setitem(action.options, "disc", None)
    monkeypatch.setitem(action.options, "track", None)
    monkeypatch.setitem(action.options, "is_original", False)

    assert not action.needs_confirmation


def test_tag_action_apply_not_actionable(monkeypatch):
    action = TagAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})

    monkeypatch.setitem(action.options, "song", None)
    monkeypatch.setitem(action.options, "disc", None)
    monkeypatch.setitem(action.options, "track", None)
    monkeypatch.setitem(action.options, "is_original", False)

    mock_mark_as_success = MagicMock()
    monkeypatch.setattr(action, "mark_as_success", mock_mark_as_success)
    mock_mark_as_fail = MagicMock()
    monkeypatch.setattr(action, "mark_as_fail", mock_mark_as_fail)

    assert not action.executed

    action.apply()

    assert not action.executed
    assert mock_mark_as_fail.call_args is None
    assert mock_mark_as_success.call_args is None


def test_tag_action_apply(monkeypatch, test_song: Song):
    monkeypatch.setattr(
        "apit.commands.tag.action.update_metadata",
        lambda *args: MagicMock(tags={"tag_id": "tag_value"}),
    )

    action = TagAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})

    monkeypatch.setitem(action.options, "song", test_song)
    monkeypatch.setitem(action.options, "disc", test_song.disc_number)
    monkeypatch.setitem(action.options, "track", test_song.track_number)
    monkeypatch.setitem(action.options, "is_original", False)
    monkeypatch.setitem(action.options, "should_backup", False)
    monkeypatch.setitem(action.options, "cover_path", None)

    action.apply()

    assert action.executed
    assert action.successful
    assert isinstance(action.result, FileTags)
    assert action.result._tags == [Mp4Tag(TagId("tag_id"), "tag_value")]


def test_tag_action_apply_error(monkeypatch, test_song: Song):
    error = ApitError("mock-error")

    def _raise(*args):
        raise error

    monkeypatch.setattr("apit.commands.tag.action.update_metadata", _raise)

    action = TagAction(Path("./tests/fixtures/folder-iteration/1 first.m4a"), {})
    monkeypatch.setitem(action.options, "song", test_song)
    monkeypatch.setitem(action.options, "disc", test_song.disc_number)
    monkeypatch.setitem(action.options, "track", test_song.track_number)
    monkeypatch.setitem(action.options, "is_original", False)
    monkeypatch.setitem(action.options, "should_backup", False)
    monkeypatch.setitem(action.options, "cover_path", None)

    action.apply()

    assert action.executed
    assert not action.successful
    assert action.result == error
