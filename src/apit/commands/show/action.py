from apit.action import Action
from apit.atomic_parser import read_metadata
from apit.error import ApitError


class ReadAction(Action):
    @property
    def needs_confirmation(self) -> bool:
        return False

    @property
    def actionable(self) -> bool:
        return True

    def apply(self) -> None:
        try:
            result = read_metadata(self.file)
        except ApitError as e:
            self.mark_as_fail(e)
        else:
            self.mark_as_success(result)
