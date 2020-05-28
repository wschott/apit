import shutil

from apit.action import Action
from apit.atomic_parser import update_metadata
from apit.error import ApitError
from apit.metadata import Song


class TagAction(Action):
    @property
    def file_matched(self) -> bool:
        return bool(self.options['disc']) and bool(self.options['track'])

    @property
    def needs_confirmation(self) -> bool:
        return self.actionable

    @property
    def actionable(self) -> bool:
        return self.file_matched and self.metadata_matched and not self.options['is_original']

    @property
    def metadata_matched(self) -> bool:
        return self.options['song'] is not None

    @property
    def song(self) -> Song:
        return self.options['song']

    def apply(self) -> None:
        if not self.actionable:
            return

        try:
            if self.options['should_backup']:
                self.backup_song()

            result = update_metadata(self.file, self.song, self.options['cover_path'])
        except ApitError as e:
            self.mark_as_fail(e)
        else:
            self.mark_as_success(result)

    def backup_song(self) -> None:
        backup_file_path = self.file.parent / f'{self.file.stem}.bak{self.file.suffix}'
        shutil.copy2(self.file, backup_file_path)
