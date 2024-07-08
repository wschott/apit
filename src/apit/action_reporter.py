from typing import Protocol

from rich.table import Table

from apit.action import Action


class ActionReporter(Protocol):
    def __init__(self, action: Action, verbose: bool) -> None: ...

    @property
    def preview_msg(self) -> str: ...

    @property
    def status_msg(self) -> str: ...

    @property
    def result(self) -> str | Table: ...
