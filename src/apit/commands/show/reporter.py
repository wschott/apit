from apit.commands.show.action import ReadAction
from apit.error import ApitError
from apit.report_action import ActionReporter


class ReadActionReporter(ActionReporter):
    def __init__(self, action: ReadAction):
        self.action = action

    @property
    def not_actionable_msg(self) -> str:
        return ""

    @property
    def preview_msg(self) -> str:
        return ""

    @property
    def status_msg(self) -> str:
        if not self.action.successful:
            return "[error]"
        if self.action.successful:
            return "successful"
        raise ApitError("Invalid state")  # TODO refactor
