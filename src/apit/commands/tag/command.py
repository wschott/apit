import logging
from collections.abc import Iterable
from collections.abc import Mapping
from pathlib import Path

from .action import TagAction
from .command_reporter import print_actions_preview
from apit.action import all_actions_successful
from apit.action import any_action_needs_confirmation
from apit.cache import save_artwork_to_cache
from apit.cache import save_metadata_to_cache
from apit.command_result import CommandResult
from apit.error import ApitError
from apit.file_handling import extract_disc_and_track_number
from apit.file_handling import generate_artwork_filename
from apit.file_handling import generate_cache_filename
from apit.file_handling import MIME_TYPE
from apit.metadata import find_song
from apit.metadata import Song
from apit.report import print_report
from apit.store.connection import download_artwork
from apit.store.connection import download_metadata
from apit.store.connection import generate_lookup_url_by_url
from apit.store.data_parser import extract_songs
from apit.tagging.read import is_itunes_bought_file
from apit.url_utils import is_url
from apit.user_input import ask_user_for_confirmation


def execute(
    files: Iterable[Path],
    verbose_level: int,
    source: str,
    has_backup_flag: bool,
    has_search_result_cache_flag: bool,
    cache_path: Path,
    has_embed_artwork_flag: bool,
    artwork_size: int,
) -> CommandResult:
    pre_action_options = to_pre_action_options(
        source=source,
        has_backup_flag=has_backup_flag,
        has_search_result_cache_flag=has_search_result_cache_flag,
        cache_path=cache_path,
        has_embed_artwork_flag=has_embed_artwork_flag,
        artwork_size=artwork_size,
    )

    actions: list[TagAction] = [
        TagAction(file, to_action_options(file, pre_action_options)) for file in files
    ]

    if any_action_needs_confirmation(actions):
        print_actions_preview(actions)
        ask_user_for_confirmation()

    for action in actions:
        print("Executing:", action)
        action.apply()

    print_report(actions, verbose=verbose_level > 0)
    return (
        CommandResult.SUCCESS if all_actions_successful(actions) else CommandResult.FAIL
    )


def to_pre_action_options(
    source: str,
    has_backup_flag: bool,
    has_search_result_cache_flag: bool,
    cache_path: Path,
    has_embed_artwork_flag: bool,
    artwork_size: int,
) -> Mapping[str, list[Song] | bool | Path | None]:
    metadata_json = get_metadata_json(source)

    songs = extract_songs(metadata_json)

    first_song = songs[0]  # TODO refactor # TODO fix possible IndexError

    if has_search_result_cache_flag and is_url(source):
        # TODO find better location for this code
        if not songs:
            raise ApitError("Failed to generate a cache filename due to missing song")
        metadata_cache_file = generate_cache_filename(cache_path, first_song)
        save_metadata_to_cache(metadata_json, metadata_cache_file)
        logging.info("Downloaded metadata cached in: %s", metadata_cache_file)

    artwork_path = None
    if has_embed_artwork_flag:
        artwork_path = get_cached_artwork_path_if_exists(first_song, cache_path)

        if artwork_path:
            logging.info("Use cached cover: %s", artwork_path)
        else:
            size = artwork_size
            upscaled_url = upscale_artwork_url(first_song, size)
            logging.info("Use cover link (with size %d): %s", size, upscaled_url)
            logging.info("Download cover (with size %d) from: %s", size, upscaled_url)
            if has_search_result_cache_flag:
                artwork_cache_path = cache_path
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
        "should_backup": has_backup_flag,
        "cover_path": artwork_path,
    }


def to_action_options(
    file: Path, options
) -> Mapping[str, Song | bool | int | Path | None]:
    disc, track = extract_disc_and_track_number(file)

    return {
        "song": find_song(options["songs"], disc=disc, track=track),
        "disc": disc,
        "track": track,
        "is_original": is_itunes_bought_file(file),
        "should_backup": options["should_backup"],
        "cover_path": options["cover_path"],
    }


def upscale_artwork_url(song: Song, size: int) -> str:
    return song.artwork_url.replace("100x100", f"{size}x{size}")


def get_cached_artwork_path_if_exists(song: Song, cache_path: Path) -> Path | None:
    jpeg_path = generate_artwork_filename(cache_path, song, MIME_TYPE.JPEG)
    png_path = generate_artwork_filename(cache_path, song, MIME_TYPE.PNG)
    if jpeg_path.exists():
        return jpeg_path
    elif png_path.exists():
        return png_path
    return None


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
    raise ApitError(f"Invalid input source: {source}")
