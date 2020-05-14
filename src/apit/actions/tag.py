import logging
from pathlib import Path
from typing import List, Mapping, Union

from apit.atomic_parser import is_itunes_bought_file, update_metadata
from apit.error import ApitError
from apit.file_handling import extract_disc_and_track_number
from apit.metadata import Album, Song, find_song
from apit.metadata_cache import generate_cache_filename, save_to_cache
from apit.store.connection import (
    download_metadata,
    generate_metadata_lookup_url,
)
from apit.store_data_parser import extract_songs
from apit.user_input import ask_user_for_input

from .base import Action


class TagAction(Action):
    COMMAND_NAME: str = 'tag'

    def __init__(self, file: Path, options: Mapping[str, Union[List[Song], bool]]):
        super().__init__(file, options)

        self._is_original = is_itunes_bought_file(self.file)
        self._file_match = extract_disc_and_track_number(self.file)
        self._song = find_song(self.options['songs'], disc=self._file_match.disc, track=self._file_match.track)

    @property
    def needs_confirmation(self) -> bool:
        return self.actionable

    @property
    def actionable(self) -> bool:
        return self._file_match.valid and self.metadata_matched and not self._is_original

    @property
    def metadata_matched(self) -> bool:
        return self._song is not None

    @property
    def song(self) -> Song:
        return self._song

    def apply(self) -> None:
        if not self.actionable:
            return

        command_status = update_metadata(self.file, self.song, self.options['should_overwrite'])

        if not bool(command_status.returncode):
            self.mark_as_success(command_status)
        else:
            self.mark_as_fail(command_status)

    @property
    def not_actionable_msg(self) -> str:
        if not self._file_match.valid:
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
        return self.song.title

    @property
    def status_msg(self) -> str:
        if not self.actionable:
            return f'[skipped: {self.not_actionable_msg}]'
        if not self.successful:
            return '[error]'
        return 'tagged'

    @staticmethod
    def to_action_options(options) -> Mapping[str, Union[List[Song], bool]]:
        source: str = options.source

        if not source:
            source = ask_user_for_input(
                question='Input Apple Music/iTunes Store URL (starts with https://music.apple.com/...): ',
                abortion='Incompatible Apple Music/iTunes Store URL provided'
            )

        metadata_json = get_metadata_json(source)

        songs = extract_songs(metadata_json)

        if options.has_search_result_cache_flag and is_url(source):
            # TODO find better location for this code
            if not len(songs):
                raise ApitError('Failed to generate a cache filename due to missing song')
            cache_file = generate_cache_filename(options.cache_path, songs[0])
            save_to_cache(metadata_json, cache_file)
            logging.info('Downloaded metadata cached in: %s', cache_file)

        return {'songs': songs, 'should_overwrite': options.has_overwrite_flag}


def is_url(source: str) -> bool:
    return source.startswith('http')


def get_metadata_json(source: str) -> str:
    logging.info('Input source: %s', source)
    if is_url(source):
        logging.info('Use URL to download metadata: %s', source)
        query_url = generate_metadata_lookup_url(source)
        logging.info('Query URL: %s', query_url)
        return download_metadata(query_url)
    elif Path(source).exists():
        logging.info('Use downloaded metadata file: %s', source)
        return Path(source).read_text()
    else:
        raise ApitError(f"Invalid input source: {source}")
