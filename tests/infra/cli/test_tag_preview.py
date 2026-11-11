from apit.infra.cli.tag_preview import _is_actionable
from apit.infra.cli.tag_preview import _to_color_for_preview
from apit.infra.cli.tag_preview import STR_NOT_SELECTED
from apit.infra.cli.tag_preview import STR_SELECTED
from apit.infra.cli.console import Color


def test_to_color_for_preview(
    mock_action_exact_match,
    mock_action_differing_match,
    mock_action_not_actionable,
):
    assert _to_color_for_preview(mock_action_not_actionable) == Color.RED
    assert _to_color_for_preview(mock_action_exact_match) == Color.GREEN
    assert _to_color_for_preview(mock_action_differing_match) == Color.YELLOW


def test_is_selected(mock_action_actionable, mock_action_not_actionable):
    assert _is_actionable(mock_action_actionable) == STR_SELECTED
    assert _is_actionable(mock_action_not_actionable) == STR_NOT_SELECTED
