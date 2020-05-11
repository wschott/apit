import logging
from pathlib import Path
from typing import Any, Dict

from apit.atomic_parser import is_itunes_bought_file, update_metadata
from apit.error import ApitError
from apit.file_handling import extract_disc_and_track_number
from apit.metadata import Album, Song
from apit.metadata_cache import save_to_cache
from apit.musicdata import (
    extract_album_with_songs,
    fetch_store_json,
    generate_store_lookup_url,
)
from apit.user_input import ask_user_for_input

from .base import Action


class TagAction(Action):
    COMMAND_NAME: str = 'tag'

    def __init__(self, file: Path, options):
        super().__init__(file, options)

        self.album: Album = self.options['album']
        self.is_original = is_itunes_bought_file(self.file)
        self.file_match = extract_disc_and_track_number(self.file)

    @property
    def needs_confirmation(self) -> bool:
        return self.actionable

    @property
    def actionable(self) -> bool:
        return self.file_match.valid and self.metadata_matched and not self.is_original

    @property
    def metadata_matched(self) -> bool:
        return self.album.has_song(disc=self.file_match.disc, track=self.file_match.track)

    @property
    def song(self) -> Song:
        return self.album.get_song(disc=self.file_match.disc, track=self.file_match.track)

    @property
    def successful(self) -> bool:
        return self.executed and not bool(self.commandStatus.returncode)

    def apply(self) -> None:
        if not self.actionable:
            return

        self.commandStatus = update_metadata(self.file, self.album, self.song, self.options['should_overwrite'])
        self._executed = True

    @property
    def not_actionable_msg(self) -> str:
        if not self.file_match.valid:
            return 'filename not matchable'
        elif self.is_original:
            return 'original iTunes Store file'
        elif not self.metadata_matched:
            return 'file not matched against metadata'
        raise NotImplementedError
        # TODO return '?'

    @property
    def preview_msg(self) -> str:
        if not self.actionable:
            return f'[{self.not_actionable_msg}]'
        return self.song["trackCensoredName"]

    @property
    def status_msg(self) -> str:
        if not self.actionable:
            return f'[skipped: {self.not_actionable_msg}]'
        if not self.successful:
            return '[error]'
        return 'tagged'

    @staticmethod
    def to_action_options(options) -> Dict[str, Any]:
        source: str = options.source

        if not source:
            source = ask_user_for_input(
                question='Input Apple Music/iTunes Store URL (starts with https://music.apple.com/...): ',
                abortion='Incompatible Apple Music/iTunes Store URL provided'
            )

        metadata_json = get_metadata_json(source)

        album = extract_album_with_songs(metadata_json)

        if options.has_search_result_cache_flag and is_url(source):
            # TODO find better location for this code
            save_to_cache(metadata_json, options.cache_path, album)

        return {'album': album, 'should_overwrite': options.has_overwrite_flag}

def is_url(source: str) -> bool:
    return source.startswith('http')

def get_metadata_json(source) -> str:
    logging.info('Input source: %s', source)
    if is_url(source):
        logging.info('Use URL to download metadata: %s', source)
        query_url = generate_store_lookup_url(source)
        logging.info('Query URL: %s', query_url)
        return fetch_store_json(query_url)
    elif Path(source).exists():
        logging.info('Use downloaded metadata file: %s', source)
        return Path(source).read_text()
    else:
        raise ApitError(f"Invalid input source: {source}")
