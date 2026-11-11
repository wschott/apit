from collections.abc import Iterable
from typing import Final

from rich.table import Column

from apit.core.track_matching import MatchQuality
from apit.infra.cli.console import Color
from apit.infra.cli.console import console
from apit.infra.cli.table import tag_preview_table
from apit.infra.cli.tag_reporter import TagActionReporter
from apit.infra.cli.tag_reporter import TagActionView

STR_SELECTED: Final = "[✕]"
STR_NOT_SELECTED: Final = "[ ]"


def print_actions_preview(actions: Iterable[TagActionView]) -> None:
    console.print("Tagging Preview")
    console.print(
        f"- {Color.RED.bb()}red[/]    → file not actionable (metadata not found)"
    )
    console.print(f"- {Color.GREEN.bb()}green[/]  → filename matches metadata exactly")
    console.print(
        f"- {Color.YELLOW.bb()}yellow[/] → filename differs from metadata → verify match"
    )
    console.print()

    header: list[str | Column] = [
        Column("Metadata Found?", max_width=8, justify="center"),
        Column("Matching Filename?", max_width=9, justify="center"),
        "File",
        "Song",
    ]
    rows = [_to_row(action) for action in actions]
    console.print(tag_preview_table(header, rows))
    console.print()


def _to_row(action: TagActionView) -> list[str]:
    color = _to_color_for_preview(action)
    return [
        _is_actionable(action),
        _has_matching_filenames(action),
        f"{color.bb()}{action.file.name}",
        f"{color.bb()}{TagActionReporter(action, verbose=False).preview_msg}",
    ]


def _to_color_for_preview(action: TagActionView) -> Color:
    if not action.actionable:
        return Color.RED
    if action.match.quality is MatchQuality.EXACT:
        return Color.GREEN
    return Color.YELLOW


def _is_actionable(action: TagActionView) -> str:
    return STR_SELECTED if action.actionable else STR_NOT_SELECTED


def _has_matching_filenames(action: TagActionView) -> str:
    return (
        STR_SELECTED if action.match.quality is MatchQuality.EXACT else STR_NOT_SELECTED
    )
