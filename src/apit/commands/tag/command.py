import logging
from collections.abc import Iterable
from collections.abc import Mapping
from pathlib import Path

from .action import TagAction
from .command_reporter import print_actions_preview
from apit.action import all_actions_successful
from apit.action import any_action_needs_confirmation
from apit.command_result import CommandResult
from apit.error import ApitError
from apit.file_handling import extract_disc_and_track_number
from apit.metadata import Artwork
from apit.metadata import find_song
from apit.metadata import Song
from apit.mime_type import MIME_TYPE
from apit.report import print_report
from apit.store.connection import download_artwork
from apit.store.connection import download_metadata
from apit.store.connection import generate_lookup_url_by_url
from apit.store.data_parser import extract_songs
from apit.url_utils import is_url
from apit.user_input import ask_user_for_confirmation


def execute(
    files: Iterable[Path],
    verbose_level: int,
    source: str,
    has_backup_flag: bool,
    has_embed_artwork_flag: bool,
    artwork_size: int,
) -> CommandResult:
    pre_action_options = to_pre_action_options(
        source=source,
        has_backup_flag=has_backup_flag,
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
    has_embed_artwork_flag: bool,
    artwork_size: int,
) -> Mapping[str, list[Song] | bool | Artwork | None]:
    metadata_json = get_metadata_json(source)

    songs = extract_songs(metadata_json)

    first_song = songs[0]  # TODO refactor # TODO fix possible IndexError

    artwork: Artwork | None = None
    if has_embed_artwork_flag:
        size = artwork_size
        upscaled_url = upscale_artwork_url(first_song, size)
        logging.info("Use cover link (with size %d): %s", size, upscaled_url)
        logging.info("Download cover (with size %d) from: %s", size, upscaled_url)

        artwork_content, image_type = download_artwork(upscaled_url)
        artwork = Artwork(content=artwork_content, mimetype=MIME_TYPE(image_type))

    return {
        "songs": songs,
        "should_backup": has_backup_flag,
        "artwork": artwork,
    }


def to_action_options(
    file: Path, options
) -> Mapping[str, Song | bool | int | Artwork | None]:
    disc, track = extract_disc_and_track_number(file)

    return {
        "song": find_song(options["songs"], disc=disc, track=track),
        "disc": disc,
        "track": track,
        "should_backup": options["should_backup"],
        "artwork": options["artwork"],
    }


def upscale_artwork_url(song: Song, size: int) -> str:
    return song.artwork_url.replace("100x100", f"{size}x{size}")


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
