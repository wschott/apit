import logging
from enum import Enum
from pathlib import Path
from typing import List

from apit.action import (
    Action,
    filter_errors,
    filter_not_actionable,
    filter_successes,
)

PREFIX = '\033[3%dm'
SUFFIX = '\033[0m'

FILENAME_TRUNCATION_LIMIT = 60
ELLIPSIS = '…'
SEPARATOR_LENGTH = 80

TABLE_LINE_FORMAT = '[%s] %s  →  %s'
STR_SELECTED = '✕'
STR_NOT_SELECTED = ' '
STR_SUCCESS = '✓'
STR_FAIL = '✘'


class Color(Enum):
    NONE = -1
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5


def to_colored_text(text: str, color: Color) -> str:
    if color == Color.NONE:
        return text
    return f'{PREFIX % color.value}{text}{SUFFIX}'


def truncate_filename(path: Path, length: int = FILENAME_TRUNCATION_LIMIT) -> str:
    if len(path.name) <= length:
        return path.name

    return path.name[:(length - len(ELLIPSIS))] + ELLIPSIS


def pad_with_spaces(string: str, length: int = FILENAME_TRUNCATION_LIMIT) -> str:
    return string.ljust(length, ' ')


def separator() -> str:
    return '-' * SEPARATOR_LENGTH


def preview_line(action: Action) -> str:
    text = TABLE_LINE_FORMAT % (
        _is_selected(action),
        pad_with_spaces(truncate_filename(action.file)),
        action.preview_msg
    )
    return to_colored_text(text=text, color=_to_color_for_preview(action))


def result_line(action: Action) -> str:
    text = TABLE_LINE_FORMAT % (
        _is_successful(action),
        pad_with_spaces(truncate_filename(action.file)),
        action.status_msg
    )
    return to_colored_text(text=text, color=_to_color_for_result(action))


def _is_successful(action: Action) -> str:
    return STR_SUCCESS if action.successful else STR_FAIL


def _is_selected(action: Action) -> str:
    return STR_SELECTED if action.actionable else STR_NOT_SELECTED


def _to_color_for_preview(action: Action) -> Color:
    if not action.actionable:
        return Color.YELLOW
    return Color.NONE


def _to_color_for_result(action: Action) -> Color:
    if not action.executed:
        return Color.YELLOW
    if not action.successful:
        return Color.RED
    return Color.GREEN


def print_actions_preview(actions: List[Action]) -> None:
    print('Preview:')
    print(separator())
    for action in actions:
        print(preview_line(action))
    print()


def print_report(actions: List[Action]) -> None:
    successes = filter_successes(actions)
    if successes:
        print('Process results:')
        for action in successes:
            print_processing_result(action)

    errors = filter_errors(actions)
    if errors:
        print('\nErrors during processing:')
        for action in errors:
            print_processing_result(action)

    skipped = filter_not_actionable(actions)

    print_summary(actions)
    print_summary_line(len(successes), len(errors), len(skipped))


def print_processing_result(action: Action) -> None:
    print(separator())
    print(result_line(action))
    print()
    if action.result:
        if action.successful:
            logging.info('Command: %s' % action.result.args)
            print(action.result.stdout.strip())
            logging.info('stderr: %s', action.result.stderr.strip())
            print()
        else:
            print('>> Command:')
            print(action.result.args)
            print('>> stdout:')
            print(action.result.stdout.strip())
            print('>> stderr:')
            print(action.result.stderr.strip())


def print_summary(actions: List[Action]) -> None:
    print('\nSummary:')
    print(separator())
    for action in actions:
        print(result_line(action))


def print_summary_line(successes: int, errors: int, skipped: int) -> None:
    summary = []
    if successes:
        summary.append(to_colored_text(f'{successes} processed', Color.GREEN))
    if errors:
        summary.append(to_colored_text(f'{errors} failed', Color.RED))
    if skipped:
        summary.append(to_colored_text(f'{skipped} skipped', Color.YELLOW))

    bar_color = Color.GREEN
    if errors:
        bar_color = Color.RED
    elif skipped:
        bar_color = Color.YELLOW

    summary_text = f" {', '.join(summary)} "
    print('\n' + to_colored_text('=' * 30, bar_color) + summary_text + to_colored_text('=' * 30, bar_color))
