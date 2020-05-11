from typing import Any, Dict

from apit.atomic_parser import read_metadata

from .base import Action


class ReadAction(Action):
    COMMAND_NAME: str = 'show'

    @property
    def needs_confirmation(self) -> bool:
        return False

    @property
    def actionable(self) -> bool:
        return True

    @property
    def successful(self) -> bool:
        return self._success

    def apply(self) -> None:
        self.commandStatus = read_metadata(self.file)
        self._executed = True
        self._success = not bool(self.commandStatus.returncode)

    @property
    def preview_msg(self) -> str:
        return ''

    @property
    def status_msg(self) -> str:
        if not self.successful:
            return '[error]'
        return 'successful'

    @staticmethod
    def to_action_options(options) -> Dict[str, Any]:
        return {}
