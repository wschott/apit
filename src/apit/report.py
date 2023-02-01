from collections.abc import Iterable

from apit.action import Action
from apit.action import filter_errors
from apit.action import filter_not_actionable
from apit.action import filter_successes
from apit.action_reporter import ActionReporter
from apit.console import Color
from apit.console import console
from apit.console import Icon
from apit.errors import ApitError


def print_report(
    actions: Iterable[Action],
    action_reporter_type: type[ActionReporter],
    verbose: bool = False,
) -> None:
    successes = filter_successes(actions)
    for action in successes:
        print_action_result(action, action_reporter_type, verbose)

    errors = filter_errors(actions)
    if errors:
        console.rule("Errors", style=Color.RED)
        for action in errors:
            print_action_result(action, action_reporter_type, verbose)

    skipped = filter_not_actionable(actions)
    if skipped:
        console.rule("Skipped", style=Color.YELLOW)
        for action in skipped:
            print_action_result(action, action_reporter_type, verbose)

    console.rule(
        "Summary", style=to_summary_line_color(errors=len(errors), skipped=len(skipped))
    )
    for action in actions:
        console.print(to_action_summary(action))


def print_action_result(
    action: Action, action_reporter_type: type[ActionReporter], verbose: bool
) -> None:
    console.print(to_action_bar(action))
    console.print()
    console.print(action_reporter_type(action, verbose).result)
    console.print()


def to_summary_line_color(errors: int, skipped: int) -> Color:
    if errors:
        return Color.RED
    if skipped:
        return Color.YELLOW
    return Color.GREEN


def to_action_bar(action: Action) -> str:
    icon, color = _to_result_styling(action)
    return f"{color.black_on()}[{icon}] {action.file.name}"


def to_action_summary(action: Action) -> str:
    icon, color = _to_result_styling(action)
    return f"{color.bb()}[{icon}] {action.file.name}"


def _to_result_styling(action: Action) -> tuple[Icon, Color]:
    if not action.successful:
        return Icon.ERROR, Color.RED
    if not action.executed:
        return Icon.ERROR, Color.YELLOW
    if action.successful:
        return Icon.OK, Color.GREEN
    raise ApitError("Unknown action state")
