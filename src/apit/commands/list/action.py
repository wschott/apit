from apit.action import Action
from apit.errors import ApitError
from apit.file_tags import FileTags
from apit.file_types import AudioFileFactory


class ReadAction(Action):
    @property
    def needs_confirmation(self) -> bool:  # TODO delete? not used anyway
        return False

    @property
    def actionable(self) -> bool:
        return True

    def apply(self) -> None:
        try:
            result: FileTags = AudioFileFactory.load(self.file).read()
        except ApitError as e:
            self.mark_as_fail(e)
        else:
            self.mark_as_success(result)
