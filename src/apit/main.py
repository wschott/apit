import logging
from pathlib import Path
from typing import Any, List, Mapping, Type

from apit.actions import (
    AVAILAIBLE_ACTIONS,
    Action,
    all_actions_successful,
    any_action_needs_confirmation,
    find_action_type,
)
from apit.defaults import CACHE_PATH, FILE_FILTER
from apit.error import ApitError
from apit.file_handling import collect_files
from apit.logger import ColoredFormatter
from apit.report import print_actions_preview, print_report
from apit.user_input import ask_user_for_confirmation


def main(options) -> int:
    configure_logging(options.verbose_level)

    logging.info('CLI options: %s', options)

    files = collect_files(options.path, FILE_FILTER)
    if len(files) == 0:
        raise ApitError('No matching files found')
    logging.info('Input path: %s', options.path)

    options.cache_path = Path(CACHE_PATH).expanduser()

    ActionType: Type[Action] = find_action_type(options.command, AVAILAIBLE_ACTIONS)

    action_options: Mapping[str, Any] = ActionType.to_action_options(options)
    actions: List[Action] = [ActionType(file, action_options) for file in files]

    if any_action_needs_confirmation(actions):
        print_actions_preview(actions)
        ask_user_for_confirmation()

    for action in actions:
        print('Executing:', action)
        action.apply()

    print_report(actions)
    return 0 if all_actions_successful(actions) else 1


def configure_logging(verbose_level: int) -> None:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter('%(levelname)s: %(message)s'))

    VERBOSITY_TO_LOG_LEVEL_MAPPING = {
        1: logging.INFO,
        2: logging.DEBUG,  # TODO not used anymore
    }

    log_level = VERBOSITY_TO_LOG_LEVEL_MAPPING.get(verbose_level, logging.WARN)
    logging.basicConfig(level=log_level, handlers=[console_handler])
