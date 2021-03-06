from pathlib import Path

from apit.commands.show.action import ReadAction
from apit.commands.show.reporter import ReadActionReporter


def test_init():
    action = ReadAction(Path('dummy.m4a'), {})
    reporter = ReadActionReporter(action)

    assert reporter.preview_msg == ''
    assert reporter.not_actionable_msg == ''
    assert reporter.status_msg == '[error]'  # TODO correct?


def test_successful():
    action = ReadAction(Path('dummy.m4a'), {})
    action.mark_as_success('test-success')
    reporter = ReadActionReporter(action)

    assert reporter.status_msg == 'successful'


def test_not_successful():
    action = ReadAction(Path('dummy.m4a'), {})
    action.mark_as_fail('test-error')
    reporter = ReadActionReporter(action)

    assert reporter.status_msg == '[error]'
