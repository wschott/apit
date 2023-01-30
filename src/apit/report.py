from collections.abc import Iterable

from apit.action import Action
from apit.action import filter_errors
from apit.action import filter_not_actionable
from apit.action import filter_successes
from apit.action_reporter import ActionReporter
from apit.color import Color
from apit.color import to_colored_text
from apit.reporting.summary import to_summary_line
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


def result_line(action: Action, action_reporter_type: type[ActionReporter]) -> str:
    text = TABLE_LINE_FORMAT % (
        _is_successful(action),
        pad_with_spaces(
            truncate_filename(normalize_unicode(action.file.name)),
            FILENAME_TRUNCATION_LIMIT,
        ),
        action_reporter_type(action, verbose=False).status_msg,
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


def print_report(
    actions: Iterable[Action],
    action_reporter_type: type[ActionReporter],
    verbose: bool = False,
) -> None:
    successes = filter_successes(actions)
    if successes:
        for action in successes:
            action_reporter = action_reporter_type(action, verbose)
            print(result_line(action, action_reporter_type))
            print()
            print(action_reporter.result)
            print()
            print()

    errors = filter_errors(actions)
    if errors:
        print(to_colored_text("Errors during processing:", color=Color.RED))
        print(separator())
        for action in errors:
            action_reporter = action_reporter_type(action, verbose)
            print(result_line(action, action_reporter_type))
            print()
            print(action_reporter.result)
            print()
            print()

    skipped = filter_not_actionable(actions)

    print()
    print("Summary:")
    print(separator())
    print("\n".join(result_line(action, action_reporter_type) for action in actions))
    print()
    print(to_summary_line(len(successes), len(errors), len(skipped)))
