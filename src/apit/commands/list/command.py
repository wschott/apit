import logging
from collections.abc import Iterable
from pathlib import Path

from .action import ReadAction
from apit.core.action import all_actions_successful
from apit.core.result import Result
from apit.infra.cli.list_reporter import ReadActionReporter
from apit.infra.cli.report import print_report


def execute(files: Iterable[Path], verbose_level: int) -> Result:
    actions: list[ReadAction] = [ReadAction(file) for file in files]

    for action in actions:
        logging.info("Executing: %s", action)
        action.apply()

    print_report(actions, ReadActionReporter, verbose=verbose_level > 0)
    return Result.SUCCESS if all_actions_successful(actions) else Result.FAIL
