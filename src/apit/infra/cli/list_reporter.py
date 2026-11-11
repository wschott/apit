from typing import override

from rich.table import Table

from apit.core.action import Action
from apit.core.errors import ApitError
from apit.infra.cli.action_reporter import ActionReporter
from apit.infra.cli.tags_report import to_tags_report


class ReadActionReporter(ActionReporter):
    def __init__(self, action: Action, verbose: bool):
        self.action = action
        self.verbose = verbose

    @property
    @override
    def preview_msg(self) -> str:
        return ""

    @property
    @override
    def status_msg(self) -> str:
        if not self.action.successful:
            return "<error>"
        if self.action.successful:
            return "successful"
        raise ApitError("Invalid state")  # TODO refactor

    @property
    @override
    def result(self) -> str | Table:
        if self.action.executed and self.action.successful and self.action.result:
            if self.action.result.has_tags:
                return to_tags_report(self.action.result, self.verbose)
            else:
                return "No tags present"
        return f"{self.status_msg} {self.action.result}"
