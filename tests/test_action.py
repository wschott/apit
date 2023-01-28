from pathlib import Path
from unittest.mock import patch

import pytest

from apit.action import Action
from apit.action import all_actions_successful
from apit.action import any_action_needs_confirmation
from apit.action import filter_errors
from apit.action import filter_not_actionable
from apit.action import filter_successes
from apit.error import ApitError


class FakeAction(Action):
    def apply(self) -> None:
        if str(self.file) == "fail":
            self.mark_as_fail(ApitError("fail"))
        elif str(self.file) == "success":
            self.mark_as_success("success")

    @property
    def actionable(self) -> bool:
        return True

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


@patch.multiple(Action, __abstractmethods__=set())
def test_action_init():
    action = Action(Path("file-path"))

    assert action.file == Path("file-path")

    assert not action.executed
    assert not action.successful
    assert not action.result

    with pytest.raises(NotImplementedError):
        action.apply()
    with pytest.raises(NotImplementedError):
        action.needs_confirmation
    with pytest.raises(NotImplementedError):
        action.actionable


def test_action_mark_as_success():
    action = FakeAction(Path("success"))

    action.apply()

    assert action.executed
    assert action.successful
    assert action.result == "success"


def test_action_mark_as_fail():
    action = FakeAction(Path("fail"))

    action.apply()

    assert action.executed
    assert not action.successful
    assert str(action.result) == "fail"
