from collections.abc import Sequence
from pathlib import Path

from .action import ReadAction
from apit.action import all_actions_successful
from apit.command import Command
from apit.command_result import CommandResult
from apit.report import print_report


class ShowCommand(Command):
    def execute(self, files: Sequence[Path], options) -> CommandResult:
        actions: Sequence[ReadAction] = [ReadAction(file, {}) for file in files]

        for action in actions:
            print("Executing:", action)
            action.apply()

        print_report(actions)
        return (
            CommandResult.SUCCESS
            if all_actions_successful(actions)
            else CommandResult.FAIL
        )
