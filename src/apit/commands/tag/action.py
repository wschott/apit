from pathlib import Path
from typing import List, Mapping, Optional, Union

from apit.action import Action
from apit.atomic_parser import is_itunes_bought_file, update_metadata
from apit.error import ApitError
from apit.file_handling import extract_disc_and_track_number
from apit.metadata import Song


class TagAction(Action):
    def __init__(self, file: Path, options: Mapping[str, Union[List[Song], bool]]):
        super().__init__(file, options)

        self._is_original = is_itunes_bought_file(self.file)
        disc_and_track = extract_disc_and_track_number(self.file)
        self._disc: Optional[int] = None
        self._track: Optional[int] = None
        if disc_and_track is not None:
            self._disc, self._track = disc_and_track
        self._song: Optional[Song] = self.options['song']

    @property
    def file_matched(self) -> bool:
        return bool(self._disc) and bool(self._track)

    @property
    def needs_confirmation(self) -> bool:
        return self.actionable

    @property
    def actionable(self) -> bool:
        return self.file_matched and self.metadata_matched and not self._is_original

    @property
    def metadata_matched(self) -> bool:
        return self._song is not None

    @property
    def song(self) -> Song:
        return self._song

    def apply(self) -> None:
        if not self.actionable:
            return

        command_status = update_metadata(self.file, self.song, self.options['should_overwrite'], self.options['cover_path'])

        if not bool(command_status.returncode):
            self.mark_as_success(command_status)
        else:
            self.mark_as_fail(command_status)

    @property
    def not_actionable_msg(self) -> str:
        if not self.file_matched:
            return 'filename not matchable'
        elif self._is_original:
            return 'original iTunes Store file'
        elif not self.metadata_matched:
            return 'file not matched against metadata'
        raise ApitError('Unknown state')
        # TODO return '?'

    @property
    def preview_msg(self) -> str:
        if not self.actionable:
            return f'[{self.not_actionable_msg}]'
        return f'{self.song.track_number_padded} {self.song.title}'

    @property
    def status_msg(self) -> str:
        if not self.actionable:
            return f'[skipped: {self.not_actionable_msg}]'
        if not self.successful:
            return '[error]'
        return 'tagged'
