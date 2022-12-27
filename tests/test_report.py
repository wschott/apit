from pathlib import Path

from apit.report import _is_selected
from apit.report import _is_successful
from apit.report import _to_color_for_preview
from apit.report import _to_color_for_result
from apit.report import Color
from apit.report import pad_with_spaces
from apit.report import STR_FAIL
from apit.report import STR_NOT_SELECTED
from apit.report import STR_SELECTED
from apit.report import STR_SUCCESS
from apit.report import to_colored_text
from apit.report import truncate_filename


def test_to_colored_text_no_color():
    assert to_colored_text("test", Color.NONE) == "test"


def test_to_colored_text_color():
    assert to_colored_text("test", Color.RED) == "\033[31mtest\033[0m"


def test_truncate_filename():
    assert truncate_filename(Path("t.m4a"), 6) == "t.m4a"
    assert truncate_filename(Path("te.m4a"), 6) == "te.m4a"
    assert truncate_filename(Path("tes.m4a"), 6) == "tes.m…"
    assert truncate_filename(Path("test.m4a"), 6) == "test.…"


def test_pad_with_spaces():
    assert pad_with_spaces("test", length=6) == "test  "
    assert pad_with_spaces("test", length=5) == "test "
    assert pad_with_spaces("test", length=4) == "test"
    assert pad_with_spaces("test", length=3) == "test"


def test_to_color_for_result(
    mock_action_failed, mock_action_success, mock_action_not_executed
):
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
