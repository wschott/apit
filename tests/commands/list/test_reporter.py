from pathlib import Path

from apit.commands.list.action import ReadAction
from apit.commands.list.reporter import ReadActionReporter


def test_init():
    action = ReadAction(Path("dummy.m4a"))
    reporter = ReadActionReporter(action, verbose=False)

    assert reporter.preview_msg == ""
    assert reporter.status_msg == "<error>"  # TODO correct?


def test_successful():
    action = ReadAction(Path("dummy.m4a"))
    action.mark_as_success("test-success")
    reporter = ReadActionReporter(action, verbose=False)

    assert reporter.status_msg == "successful"


def test_not_successful():
    action = ReadAction(Path("dummy.m4a"))
    action.mark_as_fail("test-error")
    reporter = ReadActionReporter(action, verbose=False)

    assert reporter.status_msg == "<error>"
