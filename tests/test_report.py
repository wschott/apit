from pathlib import Path

from apit.report import (
    STR_FAIL,
    STR_NOT_SELECTED,
    STR_SELECTED,
    STR_SUCCESS,
    Color,
    _is_selected,
    _is_successful,
    _to_color_for_preview,
    _to_color_for_result,
    pad_with_spaces,
    to_colored_text,
    truncate_filename,
)


def test_to_colored_text_no_color():
    assert to_colored_text('test', Color.NONE) == 'test'


def test_to_colored_text_color():
    assert to_colored_text('test', Color.RED) == '\033[31mtest\033[0m'


def test_truncate_filename():
    assert truncate_filename(Path('t.m4a'), 6) == 't.m4a'
    assert truncate_filename(Path('te.m4a'), 6) == 'te.m4a'
    assert truncate_filename(Path('tes.m4a'), 6) == 'tes.m…'
    assert truncate_filename(Path('test.m4a'), 6) == 'test.…'


def test_pad_with_spaces():
    assert pad_with_spaces('test', length=6) == 'test  '
    assert pad_with_spaces('test', length=5) == 'test '
    assert pad_with_spaces('test', length=4) == 'test'
    assert pad_with_spaces('test', length=3) == 'test'


def test_to_color_for_result(mock_action_failed, mock_action_success, mock_action_not_executed):
    assert _to_color_for_result(mock_action_failed) == Color.RED
    assert _to_color_for_result(mock_action_not_executed) == Color.YELLOW
    assert _to_color_for_result(mock_action_success) == Color.GREEN


def test_to_color_for_preview(mock_action_actionable, mock_action_not_actionable):
    assert _to_color_for_preview(mock_action_not_actionable) == Color.YELLOW
    assert _to_color_for_preview(mock_action_actionable) == Color.NONE


def test_is_successful(mock_action_failed, mock_action_success):
    assert _is_successful(mock_action_failed) == STR_FAIL
    assert _is_successful(mock_action_success) == STR_SUCCESS


def test_is_selected(mock_action_actionable, mock_action_not_actionable):
    assert _is_selected(mock_action_actionable) == STR_SELECTED
    assert _is_selected(mock_action_not_actionable) == STR_NOT_SELECTED
