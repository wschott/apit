from apit.commands.tag.command_reporter import _is_actionable
from apit.commands.tag.command_reporter import _to_color_for_preview
from apit.commands.tag.command_reporter import STR_NOT_SELECTED
from apit.commands.tag.command_reporter import STR_SELECTED
from apit.console import Color


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


def test_is_selected(mock_action_actionable, mock_action_not_actionable):
    assert _is_actionable(mock_action_actionable) == STR_SELECTED
    assert _is_actionable(mock_action_not_actionable) == STR_NOT_SELECTED
