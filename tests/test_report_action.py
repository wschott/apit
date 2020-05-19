import pytest

from apit.report_action import ActionReporter


class TestActionReporter:
    def test_init(self):
        reporter = ActionReporter()

        with pytest.raises(NotImplementedError):
            reporter.not_actionable_msg
        with pytest.raises(NotImplementedError):
            reporter.preview_msg
        with pytest.raises(NotImplementedError):
            reporter.status_msg
