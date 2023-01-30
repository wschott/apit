from .action import ReadAction
from apit.action_reporter import ActionReporter
from apit.errors import ApitError
from apit.reporting.tags_report import to_tags_report


class ReadActionReporter(ActionReporter):
    def __init__(self, action: ReadAction, verbose: bool):
        self.action = action
        self.verbose = verbose

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

    @property
    def result(self) -> str:
        if self.action.executed and self.action.successful and self.action.result:
            if self.action.result.has_tags:
                return to_tags_report(self.action.result, self.verbose)
            else:
                return "No tags present"
        return f"{self.status_msg} {self.action.result}"
