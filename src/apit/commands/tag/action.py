import shutil

from apit.action import Action
from apit.error import ApitError
from apit.file_handling import extract_disc_and_track_number
from apit.file_handling import REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME
from apit.file_tags import FileTags
from apit.metadata import Song
from apit.string_utils import clean
from apit.string_utils import compare_normalized_caseless
from apit.tagging.update import update_tags


class TagAction(Action):
    @property
    def file_matched(self) -> bool:
        return bool(self.options["disc"]) and bool(self.options["track"])

    @property
    def needs_confirmation(self) -> bool:
        return self.actionable

    @property
    def actionable(self) -> bool:
        return self.file_matched and self.metadata_matched

    @property
    def metadata_matched(self) -> bool:
        return self.options["song"] is not None

    @property
    def is_filename_identical_to_song(self) -> bool:
        if not self.actionable:
            return False

        filename_disc, filename_track = extract_disc_and_track_number(self.file)
        filename_without_track_number = REGEX_DISC_TRACK_NUMBER_IN_SONG_NAME.sub(
            "", str(self.file.with_suffix("").name)
        )

        return (
            self.song.track_number == filename_track
            and self.song.disc_number == filename_disc
            and compare_normalized_caseless(
                clean(filename_without_track_number),
                clean(self.song.title),
            )
        )

    @property
    def song(self) -> Song:
        return self.options["song"]

    def apply(self) -> None:
        if not self.actionable:
            return

        try:
            if self.options["should_backup"]:
                self.backup_song()

            result: FileTags = update_tags(
                self.file, self.song, self.options["cover_path"]
            )
        except ApitError as e:
            self.mark_as_fail(e)
        else:
            self.mark_as_success(result)

    def backup_song(self) -> None:
        backup_file_path = self.file.parent / f"{self.file.stem}.bak{self.file.suffix}"
        shutil.copy2(self.file, backup_file_path)
