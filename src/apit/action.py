import logging
from pathlib import Path
from typing import Any


class Action:
    def __init__(self, file: Path, options):
        self.file = file
        self.options = options

        logging.info(f"{self} options: {options}")

        self._executed: bool = False
        self._success: bool | None = None
        self._result: Any | None = None

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {self.file.name!r}>"

    @property
    def executed(self) -> bool:
        return self._executed

    @property
    def successful(self) -> bool | None:
        return self._success

    @property
    def result(self):
        return self._result

    def mark_as_success(self, result) -> None:
        self._executed = True
        self._success = True
        self._result = result

    def mark_as_fail(self, result) -> None:
        self._executed = True
        self._success = False
        self._result = result

    def apply(self) -> None:
        raise NotImplementedError

    @property
    def needs_confirmation(self) -> bool:
        raise NotImplementedError

    @property
    def actionable(self) -> bool:
        raise NotImplementedError


def any_action_needs_confirmation(actions: list[Action]) -> bool:
    return any(action.needs_confirmation for action in actions)


def all_actions_successful(actions: list[Action]) -> bool:
    return all(action.successful for action in actions)


def filter_successes(actions: list[Action]) -> list[Action]:
    return [action for action in actions if action.executed and action.successful]


def filter_errors(actions: list[Action]) -> list[Action]:
    return [action for action in actions if action.executed and not action.successful]


def filter_not_actionable(actions: list[Action]) -> list[Action]:
    return [action for action in actions if not action.actionable]
