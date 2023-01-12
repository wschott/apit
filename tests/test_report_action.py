from unittest.mock import patch

import pytest

from apit.report_action import ActionReporter


@patch.multiple(ActionReporter, __abstractmethods__=set())
def test_init():
    reporter = ActionReporter()

    with pytest.raises(NotImplementedError):
        reporter.not_actionable_msg
    with pytest.raises(NotImplementedError):
        reporter.preview_msg
    with pytest.raises(NotImplementedError):
        reporter.status_msg
    with pytest.raises(NotImplementedError):
        reporter.result
