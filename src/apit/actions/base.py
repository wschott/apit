from pathlib import Path
from subprocess import CompletedProcess  # TODO should not import such things
from typing import Any, List, Mapping, Optional, Type

from apit.error import ApitError


class Action:
    COMMAND_NAME: str = '_BaseAction'

    def __init__(self, file: Path, options):
        self.file = file
        self.options = options

        self._executed: bool = False
        self._success: Optional[bool] = None
        self._result: Optional[CompletedProcess] = None

    def __str__(self) -> str:
        return f'<{self.__class__.__name__} {self.file.name}>'

    @property
    def executed(self) -> bool:
        return self._executed

    @property
    def successful(self) -> bool:
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

    @property
    def not_actionable_msg(self) -> str:
        raise NotImplementedError

    @property
    def preview_msg(self) -> str:
        raise NotImplementedError

    @property
    def status_msg(self) -> str:
        raise NotImplementedError

    @staticmethod
    def to_action_options(options) -> Mapping[str, Any]:
        raise NotImplementedError


def any_action_needs_confirmation(actions: List[Action]) -> bool:
    return any(action.needs_confirmation for action in actions)


def all_actions_successful(actions: List[Action]) -> bool:
    return all(action.successful for action in actions)


def filter_successes(actions: List[Action]) -> List[Action]:
    return [action for action in actions if action.executed and action.successful]


def filter_errors(actions: List[Action]) -> List[Action]:
    return [action for action in actions if action.executed and not action.successful]


def filter_not_actionable(actions: List[Action]) -> List[Action]:
    return [action for action in actions if not action.actionable]


def find_action_type(command_name: str, action_types: List[Type[Action]]) -> Type[Action]:
    for action_type in action_types:
        if action_type.COMMAND_NAME == command_name:
            return action_type
    raise ApitError(f'Command "{command_name}" not found')
