import pytest

from apit.actions import (
    Action,
    all_actions_successful,
    any_action_needs_confirmation,
    filter_errors,
    filter_not_actionable,
    filter_successes,
)


def test_any_action_needs_confirmation(mock_action_needs_confirmation, mock_action_not_needs_confirmation):
    assert any_action_needs_confirmation([
        mock_action_not_needs_confirmation,
        mock_action_needs_confirmation,
    ])

    assert not any_action_needs_confirmation([
        mock_action_not_needs_confirmation,
        mock_action_not_needs_confirmation,
    ])


def test_all_actions_successful(mock_action_success, mock_action_failed, mock_action_not_executed):
    assert all_actions_successful([mock_action_success, mock_action_success])
    assert not all_actions_successful([mock_action_success, mock_action_failed])
    assert not all_actions_successful([mock_action_not_executed, mock_action_failed])
    assert not all_actions_successful([mock_action_not_executed, mock_action_success])


def test_filter_successes(mock_action_success, mock_action_failed, mock_action_not_executed):
    assert filter_successes([mock_action_success, mock_action_success]) == [mock_action_success, mock_action_success]
    assert filter_successes([mock_action_not_executed, mock_action_success]) == [mock_action_success]
    assert filter_successes([mock_action_failed, mock_action_success]) == [mock_action_success]
    assert filter_successes([mock_action_failed, mock_action_not_executed]) == []
    assert filter_successes([]) == []


def test_filter_errors(mock_action_success, mock_action_failed, mock_action_not_executed):
    assert filter_errors([mock_action_failed, mock_action_failed]) == [mock_action_failed, mock_action_failed]
    assert filter_errors([mock_action_not_executed, mock_action_failed]) == [mock_action_failed]
    assert filter_errors([mock_action_failed, mock_action_success]) == [mock_action_failed]
    assert filter_errors([mock_action_success, mock_action_not_executed]) == []
    assert filter_errors([]) == []


def test_filter_not_actionable(mock_action_actionable, mock_action_not_actionable):
    assert filter_not_actionable([mock_action_actionable, mock_action_actionable]) == []
    assert filter_not_actionable([mock_action_actionable, mock_action_not_actionable]) == [mock_action_not_actionable]
    assert filter_not_actionable([mock_action_not_actionable, mock_action_not_actionable]) == [mock_action_not_actionable, mock_action_not_actionable]


def test_action_to_action_options():
    with pytest.raises(NotImplementedError):
        Action.to_action_options({'test-key': 'test-value'})


def test_action_init():
    action = Action('file-path', {'test-key': 'test-value'})

    assert action.file == 'file-path'
    assert action.options == {'test-key': 'test-value'}
    assert not action.executed
    assert not action.successful
    assert not action.result

    with pytest.raises(NotImplementedError):
        action.apply()
    with pytest.raises(NotImplementedError):
        action.needs_confirmation
    with pytest.raises(NotImplementedError):
        action.actionable
    with pytest.raises(NotImplementedError):
        action.not_actionable_msg
    with pytest.raises(NotImplementedError):
        action.preview_msg
    with pytest.raises(NotImplementedError):
        action.status_msg


def test_action_mark_as_success():
    action = Action('file-path', {})

    action.mark_as_success('test-success')
    assert action.executed
    assert action.successful
    assert action.result == 'test-success'


def test_action_mark_as_fail():
    action = Action('file-path', {})

    action.mark_as_fail('test-fail')
    assert action.executed
    assert not action.successful
    assert action.result == 'test-fail'
