from pathlib import Path

from apit.commands.tag.action import TagAction
from apit.commands.tag.reporter import TagActionReporter
from apit.error import ApitError
from apit.metadata import Song


def test_not_actionable_msg_not_file_matched():
    action = TagAction(
        file=Path("dummy.m4a"), song=None, should_backup=False, artwork=None
    )

    reporter = TagActionReporter(action, verbose=False)

    assert reporter._not_actionable_msg == "filename has no matchable track number"


def test_not_actionable_msg_not_metadata_matched():
    action = TagAction(
        file=Path("1 dummy.m4a"), song=None, should_backup=False, artwork=None
    )

    reporter = TagActionReporter(action, verbose=False)

    assert reporter._not_actionable_msg == "no matching metadata found"


def test_preview_msg_not_actionable():
    action = TagAction(
        file=Path("dummy.m4a"), song=None, should_backup=False, artwork=None
    )

    reporter = TagActionReporter(action, verbose=False)

    assert reporter.preview_msg == "[filename has no matchable track number]"


def test_preview_msg_actionable(test_song: Song):
    action = TagAction(
        file=Path("2-3 dummy.m4a"), song=test_song, should_backup=False, artwork=None
    )

    reporter = TagActionReporter(action, verbose=False)

    assert reporter.preview_msg == "2-3 Track (feat. Other & $Artist) [Bonus Track]"


def test_status_msg_successful(test_song: Song):
    action = TagAction(
        file=Path("2-3 dummy.m4a"), song=test_song, should_backup=False, artwork=None
    )
    action.mark_as_success("test-success")

    reporter = TagActionReporter(action, verbose=False)

    assert reporter.status_msg == "tagged"


def test_status_msg_tag_not_successful(test_song: Song):
    action = TagAction(
        file=Path("2-3 dummy.m4a"), song=test_song, should_backup=False, artwork=None
    )
    action.mark_as_fail(ApitError("test-error"))

    reporter = TagActionReporter(action, verbose=False)

    assert reporter.status_msg == "[error]"


def test_status_msg_tag_not_actionable():
    action = TagAction(
        file=Path("dummy.m4a"), song=None, should_backup=False, artwork=None
    )

    reporter = TagActionReporter(action, verbose=False)

    assert reporter.status_msg.startswith("[skipped")
    assert reporter.status_msg.endswith("]")
