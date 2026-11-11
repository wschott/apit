from collections.abc import Mapping
from pathlib import Path
from typing import Any
from typing import Final
from typing import override
from typing import Protocol

from rich.table import Table

from apit.core.errors import ApitError
from apit.core.track_matching import Match
from apit.core.track_matching import SkipReason
from apit.infra.cli.action_reporter import ActionReporter
from apit.infra.cli.tags_report import to_tags_report


class TagActionView(Protocol):
    @property
    def file(self) -> Path: ...

    @property
    def executed(self) -> bool: ...

    @property
    def successful(self) -> bool | None: ...

    @property
    def result(self) -> Any | None: ...

    @property
    def actionable(self) -> bool: ...

    @property
    def match(self) -> Match: ...


SKIP_REASON_TEXT: Final[Mapping[SkipReason, str]] = {
    SkipReason.NO_TRACK_NUMBER: "filename has no matchable track number",
    SkipReason.NO_METADATA: "no matching metadata found",
}


class TagActionReporter(ActionReporter):
    def __init__(self, action: TagActionView, verbose: bool):
        self.action = action
        self.verbose = verbose

    @property
    def _not_actionable_msg(self) -> str:
        skip_reason = self.action.match.skip_reason
        return SKIP_REASON_TEXT[skip_reason] if skip_reason else "?"

    @property
    @override
    def preview_msg(self) -> str:
        song = self.action.match.song
        if song is None:
            return f"<{self._not_actionable_msg}>"
        return f"{song.track_number_padded} {song.title}"

    @property
    @override
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
    @override
    def result(self) -> str | Table:
        if self.action.executed and self.action.successful and self.action.result:
            return to_tags_report(self.action.result, self.verbose)
        return f"{self.status_msg} {self.action.result}"
