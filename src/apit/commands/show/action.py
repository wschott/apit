from apit.action import Action
from apit.error import ApitError
from apit.tagging.read import read_metadata


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
            if not result.tags:
                raise ApitError("No tags present")
        except ApitError as e:
            self.mark_as_fail(e)
        else:
            self.mark_as_success(result)
