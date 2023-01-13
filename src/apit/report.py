from collections.abc import Iterable

from apit.action import Action
from apit.action import filter_errors
from apit.action import filter_not_actionable
from apit.action import filter_successes
from apit.color import Color
from apit.color import to_colored_text
from apit.commands.list.action import ReadAction
from apit.commands.list.reporter import ReadActionReporter
from apit.commands.tag.action import TagAction
from apit.commands.tag.reporter import TagActionReporter
from apit.error import ApitError
from apit.report_action import ActionReporter
from apit.string_utils import normalize_unicode
from apit.string_utils import pad_with_spaces
from apit.string_utils import truncate_text

FILENAME_TRUNCATION_LIMIT = 60
SEPARATOR_LENGTH = 80

TABLE_LINE_FORMAT = "[%s] %s  →  %s"
STR_SUCCESS = "✓"
STR_FAIL = "✘"


def truncate_filename(text: str, length: int = FILENAME_TRUNCATION_LIMIT) -> str:
    return truncate_text(text, length)


def separator() -> str:
    return "-" * SEPARATOR_LENGTH


def result_line(action: Action) -> str:
    text = TABLE_LINE_FORMAT % (
        _is_successful(action),
        pad_with_spaces(
            truncate_filename(normalize_unicode(action.file.name)),
            FILENAME_TRUNCATION_LIMIT,
        ),
        to_action_reporter(action, verbose=False).status_msg,
    )
    return to_colored_text(text=text, color=_to_color_for_result(action))


def _is_successful(action: Action) -> str:
    return STR_SUCCESS if action.successful else STR_FAIL


def _to_color_for_result(action: Action) -> Color:
    if not action.executed:
        return Color.YELLOW
    if not action.successful:
        return Color.RED
    return Color.GREEN


def print_report(actions: Iterable[Action], verbose: bool = False) -> None:
    successes = filter_successes(actions)
    if successes:
        print("\nProcess results:")
        for action in successes:
            print_processing_result(action, verbose)

    errors = filter_errors(actions)
    if errors:
        print("\nErrors during processing:")
        for action in errors:
            print_processing_result(action, verbose)

    skipped = filter_not_actionable(actions)

    print_summary(actions)
    print_summary_line(len(successes), len(errors), len(skipped))


def print_processing_result(action: Action, verbose: bool) -> None:
    print()
    print()
    print(result_line(action))
    print()
    print(to_action_reporter(action, verbose).result)


def print_summary(actions: Iterable[Action]) -> None:
    print("\nSummary:")
    print(separator())
    for action in actions:
        print(result_line(action))


def print_summary_line(successes: int, errors: int, skipped: int) -> None:
    summary = []
    if successes:
        summary.append(to_colored_text(f"{successes} processed", Color.GREEN))
    if errors:
        summary.append(to_colored_text(f"{errors} failed", Color.RED))
    if skipped:
        summary.append(to_colored_text(f"{skipped} skipped", Color.YELLOW))

    bar_color = Color.GREEN
    if errors:
        bar_color = Color.RED
    elif skipped:
        bar_color = Color.YELLOW

    summary_text = f" {', '.join(summary)} "
    print(
        "\n"
        + to_colored_text("=" * 30, bar_color)
        + summary_text
        + to_colored_text("=" * 30, bar_color)
    )


def to_action_reporter(action: Action, verbose: bool) -> ActionReporter:
    if isinstance(action, ReadAction):
        return ReadActionReporter(action, verbose)
    elif isinstance(action, TagAction):
        return TagActionReporter(action, verbose)
    raise ApitError("Unknown action")
