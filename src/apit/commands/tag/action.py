from typing import override

from apit.core.action import Action
from apit.core.audio.file_tags import FileTags
from apit.core.errors import ApitError
from apit.core.metadata.artwork import Artwork
from apit.core.track_matching import Match
from apit.utils.io import backup_file
from apit.file_types import AudioFileFactory


class TagAction(Action):
    def __init__(
        self,
        match: Match,
        should_backup: bool,
        artwork: Artwork | None,
    ) -> None:
        super().__init__(match.file)

        self.match: Match = match
        self.should_backup: bool = should_backup
        self.artwork: Artwork | None = artwork

    @property
    @override
    def needs_confirmation(self) -> bool:
        return self.actionable

    @property
    @override
    def actionable(self) -> bool:
        return self.match.actionable

    @override
    def apply(self) -> None:
        if (song := self.match.song) is None:
            return

        try:
            if self.should_backup:
                self.backup_audio_file()

            result: FileTags = AudioFileFactory.load(self.file).update(
                song, self.artwork
            )
        except ApitError as e:
            self.mark_as_fail(e)
        else:
            self.mark_as_success(result)

    def backup_audio_file(self) -> None:
        backup_file(self.file)
