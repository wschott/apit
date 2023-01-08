from apit.color import Color
from apit.color import to_colored_text
from apit.commands.tag.command_reporter import _is_selected
from apit.commands.tag.command_reporter import _to_color_for_preview
from apit.commands.tag.command_reporter import STR_NOT_SELECTED
from apit.commands.tag.command_reporter import STR_SELECTED
from apit.report import _is_successful
from apit.report import _to_color_for_result
from apit.report import STR_FAIL
from apit.report import STR_SUCCESS
from apit.report import truncate_filename


def test_to_colored_text_no_color():
    assert to_colored_text("test", Color.NONE) == "test"


def test_to_colored_text_color():
    assert to_colored_text("test", Color.RED) == "\033[31mtest\033[0m"


def test_truncate_filename():
    assert truncate_filename("t.m4a", 6) == "t.m4a"
    assert truncate_filename("te.m4a", 6) == "te.m4a"
    assert truncate_filename("tes.m4a", 6) == "tes.m…"
    assert truncate_filename("test.m4a", 6) == "test.…"


def test_to_color_for_result(
    mock_action_failed, mock_action_success, mock_action_not_executed
):
    assert _to_color_for_result(mock_action_failed) == Color.RED
    assert _to_color_for_result(mock_action_not_executed) == Color.YELLOW
    assert _to_color_for_result(mock_action_success) == Color.GREEN


def test_to_color_for_preview(
    mock_action_is_filename_identical_to_song,
    mock_action_actionable_not_is_filename_identical_to_song,
    mock_action_not_actionable,
):
    assert _to_color_for_preview(mock_action_not_actionable) == Color.RED
    assert (
        _to_color_for_preview(mock_action_is_filename_identical_to_song) == Color.GREEN
    )
    assert (
        _to_color_for_preview(mock_action_actionable_not_is_filename_identical_to_song)
        == Color.YELLOW
    )


def test_is_successful(mock_action_failed, mock_action_success):
    assert _is_successful(mock_action_failed) == STR_FAIL
    assert _is_successful(mock_action_success) == STR_SUCCESS


def test_is_selected(mock_action_actionable, mock_action_not_actionable):
    assert _is_selected(mock_action_actionable) == STR_SELECTED
    assert _is_selected(mock_action_not_actionable) == STR_NOT_SELECTED
