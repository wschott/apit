from apit.action import Action
from apit.atomic_parser import read_metadata


class ReadAction(Action):
    @property
    def needs_confirmation(self) -> bool:
        return False

    @property
    def actionable(self) -> bool:
        return True

    def apply(self) -> None:
        command_status = read_metadata(self.file)

        if not bool(command_status.returncode):
            self.mark_as_success(command_status)
        else:
            self.mark_as_fail(command_status)

    @property
    def preview_msg(self) -> str:
        return ''

    @property
    def status_msg(self) -> str:
        if not self.successful:
            return '[error]'
        return 'successful'
