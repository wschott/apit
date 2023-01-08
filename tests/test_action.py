from pathlib import Path

from apit.action import Action
from apit.action import all_actions_successful
from apit.action import any_action_needs_confirmation
from apit.action import filter_errors
from apit.action import filter_not_actionable
from apit.action import filter_successes


class TestAction(Action):
    def apply(self) -> None:
        if self.options["apply-option"] == "fail":
            self.mark_as_fail(self.options["apply-option"])
        elif self.options["apply-option"] == "success":
            self.mark_as_success(self.options["apply-option"])

    @property
    def actionable(self) -> bool:
        return "apply-option" in self.options

    @property
    def needs_confirmation(self) -> bool:
        return False


def test_any_action_needs_confirmation(
    mock_action_needs_confirmation, mock_action_not_needs_confirmation
):
    assert any_action_needs_confirmation(
        [
            mock_action_not_needs_confirmation,
            mock_action_needs_confirmation,
        ]
    )

    assert not any_action_needs_confirmation(
        [
            mock_action_not_needs_confirmation,
            mock_action_not_needs_confirmation,
        ]
    )


def test_all_actions_successful(
    mock_action_success, mock_action_failed, mock_action_not_executed
):
    assert all_actions_successful([mock_action_success, mock_action_success])
    assert not all_actions_successful([mock_action_success, mock_action_failed])
    assert not all_actions_successful([mock_action_not_executed, mock_action_failed])
    assert not all_actions_successful([mock_action_not_executed, mock_action_success])


def test_filter_successes(
    mock_action_success, mock_action_failed, mock_action_not_executed
):
    assert filter_successes([mock_action_success, mock_action_success]) == [
        mock_action_success,
        mock_action_success,
    ]
    assert filter_successes([mock_action_not_executed, mock_action_success]) == [
        mock_action_success
    ]
    assert filter_successes([mock_action_failed, mock_action_success]) == [
        mock_action_success
    ]
    assert filter_successes([mock_action_failed, mock_action_not_executed]) == []
    assert filter_successes([]) == []


def test_filter_errors(
    mock_action_success, mock_action_failed, mock_action_not_executed
):
    assert filter_errors([mock_action_failed, mock_action_failed]) == [
        mock_action_failed,
        mock_action_failed,
    ]
    assert filter_errors([mock_action_not_executed, mock_action_failed]) == [
        mock_action_failed
    ]
    assert filter_errors([mock_action_failed, mock_action_success]) == [
        mock_action_failed
    ]
    assert filter_errors([mock_action_success, mock_action_not_executed]) == []
    assert filter_errors([]) == []


def test_filter_not_actionable(mock_action_actionable, mock_action_not_actionable):
    assert filter_not_actionable([mock_action_actionable, mock_action_actionable]) == []
    assert filter_not_actionable(
        [mock_action_actionable, mock_action_not_actionable]
    ) == [mock_action_not_actionable]
    assert filter_not_actionable(
        [mock_action_not_actionable, mock_action_not_actionable]
    ) == [mock_action_not_actionable, mock_action_not_actionable]


def test_action_init():
    action = TestAction(Path("file-path"), {"test-key": "test-value"})

    assert action.file == Path("file-path")
    assert action.options == {"test-key": "test-value"}

    assert not action.executed
    assert not action.successful
    assert not action.result
    assert not action.needs_confirmation


def test_action_mark_as_success():
    action = TestAction(Path("file-path"), {"apply-option": "success"})

    action.apply()

    assert action.executed
    assert action.successful
    assert action.result == "success"


def test_action_mark_as_fail():
    action = TestAction(Path("file-path"), {"apply-option": "fail"})

    action.apply()

    assert action.executed
    assert not action.successful
    assert action.result == "fail"
