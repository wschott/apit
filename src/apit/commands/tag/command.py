import logging
import urllib.request
from pathlib import Path
from typing import List, Mapping, Optional, Union

from apit.action import (
    Action,
    all_actions_successful,
    any_action_needs_confirmation,
)
from apit.commands.base import Command
from apit.error import ApitError
from apit.file_handling import (
    MIME_TYPE,
    extract_disc_and_track_number,
    generate_artwork_filename,
    generate_cache_filename,
)
from apit.metadata import Song, find_song
from apit.metadata_cache import save_to_cache
from apit.report import print_actions_preview, print_report
from apit.store.connection import (
    download_metadata,
    generate_lookup_url_by_str,
    generate_lookup_url_by_url,
)
from apit.store_data_parser import extract_songs
from apit.user_input import ask_user_for_confirmation, ask_user_for_input

from .action import TagAction


class TagCommand(Command):
    def execute(self, files: List[Path], options):
        pre_action_options = to_pre_action_options(options)

        actions: List[Action] = [TagAction(file, to_action_options(file, pre_action_options)) for file in files]

        if any_action_needs_confirmation(actions):
            print_actions_preview(actions)
            ask_user_for_confirmation()

        for action in actions:
            print('Executing:', action)
            action.apply()

        print_report(actions)
        return 0 if all_actions_successful(actions) else 1


def to_pre_action_options(options) -> Mapping[str, Union[List[Song], bool]]:
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


def to_action_options(file: Path, options) -> Mapping[str, Union[Optional[Song], bool, Optional[int], Optional[Path]]]:
    disc_and_track = extract_disc_and_track_number(file)
    disc: Optional[int] = None
    track: Optional[int] = None
    if disc_and_track is not None:
        disc, track = disc_and_track
    song: Optional[Song] = find_song(options['songs'], disc=disc, track=track)

    return {
        'song': song,
        'disc': disc,
        'track': track,
        'should_overwrite': options['should_overwrite'],
        'cover_path': options['cover_path'],
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
        try:
            return Path(source).read_text()
        except Exception:
            raise ApitError('Error while reading metadata file: %s' % Path(source))
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
