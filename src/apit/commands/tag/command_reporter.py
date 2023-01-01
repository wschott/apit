from collections.abc import Iterable

from .action import TagAction
from .reporter import TagActionReporter
from apit.reporting.color import Color
from apit.reporting.color import to_colored_text
from apit.reporting.table import legend_table
from apit.reporting.table import tag_preview_table

STR_SELECTED = "✕"
STR_NOT_SELECTED = " "


def print_actions_preview(actions: Iterable[TagAction]) -> None:
    print("Preview:")
    print()

    print(
        legend_table(
            [
                [
                    to_colored_text("red", Color.RED),
                    "file not actionable (metadata not found)",
                ],
                [to_colored_text("green", Color.GREEN), "filename matches metadata"],
                [
                    to_colored_text("yellow", Color.YELLOW),
                    "filename doesn't match metadata -> verify match",
                ],
            ]
        )
    )
    print()

    header: list[str] = ["Metadata\nFound?", "Matching\nFilename?", "\nFile", "\nSong"]
    rows = [_to_row(action) for action in actions]
    print(tag_preview_table(header, rows))
    print()


def _to_row(action: TagAction) -> list[str]:
    color = _to_color_for_preview(action)
    return [
        _is_selected(action),
        _has_matching_filenames(action),
        to_colored_text(text=action.file.name, color=color),
        to_colored_text(text=TagActionReporter(action).preview_msg, color=color),
    ]


def _to_color_for_preview(action: TagAction) -> Color:
    if not action.actionable:
        return Color.RED
    if action.is_filename_identical_to_song:
        return Color.GREEN
    return Color.YELLOW


def _is_selected(action: TagAction) -> str:
    return STR_SELECTED if action.actionable else STR_NOT_SELECTED


def _has_matching_filenames(action: TagAction) -> str:
    return STR_SELECTED if action.is_filename_identical_to_song else STR_NOT_SELECTED
