from pathlib import Path

from apit.infra.cli.tag_reporter import TagActionReporter
from apit.core.errors import ApitError
from apit.core.metadata.song import Song
from tests.conftest import make_tag_action


def test_not_actionable_msg_not_file_matched():
    action = make_tag_action(Path("dummy.m4a"))

    reporter = TagActionReporter(action, verbose=False)

    assert reporter._not_actionable_msg == "filename has no matchable track number"


def test_not_actionable_msg_not_metadata_matched():
    action = make_tag_action(Path("1 dummy.m4a"))

    reporter = TagActionReporter(action, verbose=False)

    assert reporter._not_actionable_msg == "no matching metadata found"


def test_preview_msg_not_actionable():
    action = make_tag_action(Path("dummy.m4a"))

    reporter = TagActionReporter(action, verbose=False)

    assert reporter.preview_msg == "<filename has no matchable track number>"


def test_preview_msg_actionable(test_song: Song):
    action = make_tag_action(Path("2-3 dummy.m4a"), test_song)

    reporter = TagActionReporter(action, verbose=False)

    assert reporter.preview_msg == "2-3 Track (feat. Other & $Artist) [Bonus Track]"


def test_status_msg_successful(test_song: Song):
    action = make_tag_action(Path("2-3 dummy.m4a"), test_song)
    action.mark_as_success("test-success")

    reporter = TagActionReporter(action, verbose=False)

    assert reporter.status_msg == "tagged"


def test_status_msg_tag_not_successful(test_song: Song):
    action = make_tag_action(Path("2-3 dummy.m4a"), test_song)
    action.mark_as_fail(ApitError("test-error"))

    reporter = TagActionReporter(action, verbose=False)

    assert reporter.status_msg == "<error>"


def test_status_msg_tag_not_actionable():
    action = make_tag_action(Path("dummy.m4a"))

    reporter = TagActionReporter(action, verbose=False)

    assert reporter.status_msg.startswith("<skipped")
    assert reporter.status_msg.endswith(">")
