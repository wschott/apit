from pathlib import Path

from .action import ReadAction
from apit.action import Action
from apit.action import all_actions_successful
from apit.action import any_action_needs_confirmation
from apit.command import Command
from apit.report import print_actions_preview
from apit.report import print_report
from apit.user_input import ask_user_for_confirmation


class ShowCommand(Command):
    def execute(self, files: list[Path], options):
        actions: list[Action] = [ReadAction(file, {}) for file in files]

        if any_action_needs_confirmation(actions):
            print_actions_preview(actions)
            ask_user_for_confirmation()

        for action in actions:
            print("Executing:", action)
            action.apply()

        print_report(actions)
        return 0 if all_actions_successful(actions) else 1
