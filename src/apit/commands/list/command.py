import logging
from pathlib import Path

from .action import ReadAction
from .reporter import ReadActionReporter
from apit.action import all_actions_successful
from apit.command_result import CommandResult
from apit.report import print_report


def execute(files: list[Path], verbose_level: int) -> CommandResult:
    actions: list[ReadAction] = [ReadAction(file) for file in files]

    for action in actions:
        logging.info("Executing: %s", action)
        action.apply()

    print_report(actions, ReadActionReporter, verbose=verbose_level > 0)
    return (
        CommandResult.SUCCESS if all_actions_successful(actions) else CommandResult.FAIL
    )
