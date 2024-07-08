from rich.table import Table

from .action import TagAction
from apit.action_reporter import ActionReporter
from apit.errors import ApitError
from apit.reporting.tags_report import to_tags_report


class TagActionReporter(ActionReporter):
    def __init__(self, action: TagAction, verbose: bool):
        self.action = action
        self.verbose = verbose

    @property
    def _not_actionable_msg(self) -> str:
        if not self.action.file_matched:
            return "filename has no matchable track number"
        elif not self.action.metadata_matched:
            return "no matching metadata found"
        raise ApitError("Unknown state")
        # TODO return '?'

    @property
    def preview_msg(self) -> str:
        if not self.action.actionable:
            return f"<{self._not_actionable_msg}>"
        return f"{self.action.song.track_number_padded} {self.action.song.title}"  # type: ignore[union-attr]

    @property
    def status_msg(self) -> str:
        # TODO review conditions
        if not self.action.actionable:
            return f"<skipped: {self._not_actionable_msg}>"
        if not self.action.successful:
            return "<error>"
        if self.action.executed and self.action.successful:
            return "tagged"
        raise ApitError("Invalid state")

    @property
    def result(self) -> str | Table:
        if self.action.executed and self.action.successful and self.action.result:
            return to_tags_report(self.action.result, self.verbose)
        return f"{self.status_msg} {self.action.result}"
