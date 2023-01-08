from apit.action import Action
from apit.error import ApitError
from apit.tagging.read import read_metadata
from apit.tagging.read import to_file_tags


class ReadAction(Action):
    @property
    def needs_confirmation(self) -> bool:  # TODO delete? not used anyway
        return False

    @property
    def actionable(self) -> bool:
        return True

    def apply(self) -> None:
        try:
            result = to_file_tags(read_metadata(self.file))
        except ApitError as e:
            self.mark_as_fail(e)
        else:
            self.mark_as_success(result)
