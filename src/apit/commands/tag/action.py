from pathlib import Path

from apit.action import Action
from apit.errors import ApitError
from apit.file_handling import backup_file
from apit.file_handling import extract_disc_and_track_number
from apit.file_handling import REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME
from apit.file_tags import FileTags
from apit.file_types import AudioFileFactory
from apit.metadata import Artwork
from apit.metadata import Song
from apit.string_utils import clean
from apit.string_utils import compare_normalized_caseless
from apit.types import DiscNumber
from apit.types import TrackNumber


class TagAction(Action):
    def __init__(
        self,
        file: Path,
        song: Song | None,
        should_backup: bool,
        artwork: Artwork | None,
    ) -> None:
        super().__init__(file)

        disc, track = extract_disc_and_track_number(self.file)
        self.disc: DiscNumber | None = disc
        self.track: TrackNumber | None = track
        self.song: Song | None = song
        self.should_backup: bool = should_backup
        self.artwork: Artwork | None = artwork

    @property
    def file_matched(self) -> bool:
        return bool(self.disc) and bool(self.track)

    @property
    def needs_confirmation(self) -> bool:
        return self.actionable

    @property
    def actionable(self) -> bool:
        return self.file_matched and self.metadata_matched

    @property
    def metadata_matched(self) -> bool:
        return self.song is not None

    @property
    def is_filename_identical_to_song(self) -> bool:
        if not self.actionable:
            return False

        filename_without_track_number = REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME.sub(
            "", str(self.file.with_suffix("").name)
        )

        return (
            self.song.track_number == self.track  # type: ignore[union-attr]
            and self.song.disc_number == self.disc  # type: ignore[union-attr]
            and compare_normalized_caseless(
                clean(filename_without_track_number),
                clean(self.song.title),  # type: ignore[union-attr]
            )
        )

    def apply(self) -> None:
        if not self.actionable:
            return

        try:
            if self.should_backup:
                self.backup_song()

            result: FileTags = AudioFileFactory.load(self.file).update(
                self.song,  # type: ignore[arg-type]
                self.artwork,
            )
        except ApitError as e:
            self.mark_as_fail(e)
        else:
            self.mark_as_success(result)

    def backup_song(self) -> None:
        backup_file(self.file)
