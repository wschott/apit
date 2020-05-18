import logging
import urllib.request
from pathlib import Path
from typing import List, Mapping, Optional, Union

from apit.atomic_parser import is_itunes_bought_file, update_metadata
from apit.error import ApitError
from apit.file_handling import (
    MIME_TYPE,
    extract_disc_and_track_number,
    generate_artwork_filename,
    generate_cache_filename,
)
from apit.metadata import Song, find_song
from apit.metadata_cache import save_to_cache
from apit.store.connection import (
    download_metadata,
    generate_lookup_url_by_str,
    generate_lookup_url_by_url,
)
from apit.store_data_parser import extract_songs
from apit.user_input import ask_user_for_input

from .base import Action


class TagAction(Action):
    COMMAND_NAME: str = 'tag'

    def __init__(self, file: Path, options: Mapping[str, Union[List[Song], bool]]):
        super().__init__(file, options)

        self._is_original = is_itunes_bought_file(self.file)
        disc_and_track = extract_disc_and_track_number(self.file)
        self._disc: Optional[int] = None
        self._track: Optional[int] = None
        if disc_and_track is not None:
            self._disc, self._track = disc_and_track
        self._song: Optional[Song] = find_song(self.options['songs'], disc=self._disc, track=self._track)

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

        first_song = songs[0]  # TODO refactor # TODO fix possible IndexError

        if options.has_search_result_cache_flag and is_url(source):
            # TODO find better location for this code
            if not len(songs):
                raise ApitError('Failed to generate a cache filename due to missing song')
            cache_file = generate_cache_filename(options.cache_path, first_song)
            save_to_cache(metadata_json, cache_file)
            logging.info('Downloaded metadata cached in: %s', cache_file)

        cover_path = None
        if options.has_embed_artwork_flag:
            cover_path = get_cached_artwork_path_if_exists(first_song, options)

            if cover_path:
                logging.info('Use cached cover: %s', cover_path)
            else:
                size = options.artwork_size
                upscaled_url = upscale_artwork_url(first_song, size)
                logging.info('Use cover link (with size %d): %s', size, upscaled_url)
                logging.info('Download cover (with size %d) from: %s', size, upscaled_url)
                if options.has_search_result_cache_flag:
                    artwork_cache_path = options.cache_path
                else:
                    import tempfile
                    autodeleting_temp_path = tempfile.TemporaryDirectory()
                    artwork_cache_path = Path(autodeleting_temp_path.name)
                cover_path = download_artwork(upscaled_url, artwork_cache_path, first_song)
                logging.info('Cover cached in: %s', cover_path)

        return {
            'songs': songs,
            'should_overwrite': options.has_overwrite_flag,
            'cover_path': cover_path,
        }


def download_artwork(url, cache_path, song) -> Path:
    with urllib.request.urlopen(url) as response:
        # TODO HTTP error handling
        content_type = response.getheader('Content-Type')
        logging.info('Headers: %s', response.info())
        try:
            image_type = MIME_TYPE(content_type)
        except ValueError:
            raise ApitError('Unknown artwork content type: %s' % content_type)
        else:
            cover_path = generate_artwork_filename(cache_path, song, image_type)
        cover_path.write_bytes(response.read())
    return cover_path


def upscale_artwork_url(song, size):
    return song.artwork_url.replace('100x100', f'{size}x{size}')


def get_cached_artwork_path_if_exists(song, options) -> Optional[Path]:
    jpeg_path = generate_artwork_filename(options.cache_path, song, MIME_TYPE.JPEG)
    png_path = generate_artwork_filename(options.cache_path, song, MIME_TYPE.PNG)
    if jpeg_path.exists():
        return jpeg_path
    elif png_path.exists():
        return png_path
    return None


def is_url(source: str) -> bool:
    return source.startswith('http')


def get_metadata_json(source: str) -> str:
    logging.info('Input source: %s', source)
    if Path(source).exists():
        logging.info('Use downloaded metadata file: %s', source)
        return Path(source).read_text()
    elif is_url(source):
        logging.info('Use URL to download metadata: %s', source)
        query_url = generate_lookup_url_by_url(source)
        logging.info('Query URL: %s', query_url)
        return download_metadata(query_url)
    elif isinstance(source, str):
        logging.info('Use URL composition to download metadata: %s', source)
        query_url = generate_lookup_url_by_str(source)
        logging.info('Query URL: %s', query_url)
        return download_metadata(query_url)
    raise ApitError(f"Invalid input source: {source}")
