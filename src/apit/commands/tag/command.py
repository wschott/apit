import logging
from collections.abc import Mapping
from pathlib import Path

from .action import TagAction
from apit.action import Action
from apit.action import all_actions_successful
from apit.action import any_action_needs_confirmation
from apit.atomic_parser import is_itunes_bought_file
from apit.cache import save_artwork_to_cache
from apit.cache import save_metadata_to_cache
from apit.command import Command
from apit.error import ApitError
from apit.file_handling import extract_disc_and_track_number
from apit.file_handling import generate_artwork_filename
from apit.file_handling import generate_cache_filename
from apit.file_handling import MIME_TYPE
from apit.metadata import find_song
from apit.metadata import Song
from apit.report import print_actions_preview
from apit.report import print_report
from apit.store.connection import download_artwork
from apit.store.connection import download_metadata
from apit.store.connection import generate_lookup_url_by_str
from apit.store.connection import generate_lookup_url_by_url
from apit.store_data_parser import extract_songs
from apit.user_input import ask_user_for_confirmation
from apit.user_input import ask_user_for_input


class TagCommand(Command):
    def execute(self, files: list[Path], options):
        pre_action_options = to_pre_action_options(options)

        actions: list[Action] = [
            TagAction(file, to_action_options(file, pre_action_options))
            for file in files
        ]

        if any_action_needs_confirmation(actions):
            print_actions_preview(actions)
            ask_user_for_confirmation()

        for action in actions:
            print("Executing:", action)
            action.apply()

        print_report(actions)
        return 0 if all_actions_successful(actions) else 1


def to_pre_action_options(options) -> Mapping[str, list[Song] | bool | Path | None]:
    source: str = options.source

    if not source:
        source = ask_user_for_input(
            question="Input Apple Music/iTunes Store URL (starts with https://music.apple.com/...): ",  # noqa: B950
            abortion="Incompatible Apple Music/iTunes Store URL provided",
        )

    metadata_json = get_metadata_json(source)

    songs = extract_songs(metadata_json)

    first_song = songs[0]  # TODO refactor # TODO fix possible IndexError

    if options.has_search_result_cache_flag and is_url(source):
        # TODO find better location for this code
        if not len(songs):
            raise ApitError("Failed to generate a cache filename due to missing song")
        metadata_cache_file = generate_cache_filename(options.cache_path, first_song)
        save_metadata_to_cache(metadata_json, metadata_cache_file)
        logging.info("Downloaded metadata cached in: %s", metadata_cache_file)

    artwork_path = None
    if options.has_embed_artwork_flag:
        artwork_path = get_cached_artwork_path_if_exists(first_song, options)

        if artwork_path:
            logging.info("Use cached cover: %s", artwork_path)
        else:
            size = options.artwork_size
            upscaled_url = upscale_artwork_url(first_song, size)
            logging.info("Use cover link (with size %d): %s", size, upscaled_url)
            logging.info("Download cover (with size %d) from: %s", size, upscaled_url)
            if options.has_search_result_cache_flag:
                artwork_cache_path = options.cache_path
            else:
                import tempfile

                artwork_cache_path = Path(tempfile.gettempdir())
            artwork_content, image_type = download_artwork(upscaled_url)
            artwork_path = generate_artwork_filename(
                artwork_cache_path, first_song, image_type
            )
            save_artwork_to_cache(artwork_content, artwork_path)
            logging.info("Cover cached in: %s", artwork_path)

    return {
        "songs": songs,
        "should_backup": options.has_backup_flag,
        "cover_path": artwork_path,
    }


def to_action_options(
    file: Path, options
) -> Mapping[str, Song | bool | int | Path | None]:
    disc_and_track = extract_disc_and_track_number(file)
    disc: int | None = None
    track: int | None = None
    if disc_and_track is not None:
        disc, track = disc_and_track

    return {
        "song": find_song(options["songs"], disc=disc, track=track),
        "disc": disc,
        "track": track,
        "is_original": is_itunes_bought_file(file),
        "should_backup": options["should_backup"],
        "cover_path": options["cover_path"],
    }


def upscale_artwork_url(song, size):
    return song.artwork_url.replace("100x100", f"{size}x{size}")


def get_cached_artwork_path_if_exists(song, options) -> Path | None:
    jpeg_path = generate_artwork_filename(options.cache_path, song, MIME_TYPE.JPEG)
    png_path = generate_artwork_filename(options.cache_path, song, MIME_TYPE.PNG)
    if jpeg_path.exists():
        return jpeg_path
    elif png_path.exists():
        return png_path
    return None


def is_url(source: str) -> bool:
    return source.startswith("http")


def get_metadata_json(source: str) -> str:
    logging.info("Input source: %s", source)
    if Path(source).exists():
        logging.info("Use downloaded metadata file: %s", source)
        try:
            return Path(source).read_text()
        except Exception:
            raise ApitError("Error while reading metadata file: %s" % Path(source))
    elif is_url(source):
        logging.info("Use URL to download metadata: %s", source)
        query_url = generate_lookup_url_by_url(source)
        logging.info("Query URL: %s", query_url)
        return download_metadata(query_url)
    elif isinstance(source, str):
        logging.info("Use URL composition to download metadata: %s", source)
        query_url = generate_lookup_url_by_str(source)
        logging.info("Query URL: %s", query_url)
        return download_metadata(query_url)
    raise ApitError(f"Invalid input source: {source}")
