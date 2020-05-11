from apit.actions import (
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
