import logging
from pathlib import Path

from .action import TagAction
from .command_reporter import print_actions_preview
from .reporter import TagActionReporter
from apit.action import all_actions_successful
from apit.action import any_action_needs_confirmation
from apit.command_result import CommandResult
from apit.errors import ApitError
from apit.file_handling import extract_disc_and_track_number
from apit.metadata import Artwork
from apit.metadata import find_song
from apit.metadata import Song
from apit.mime_type import MimeType
from apit.report import print_report
from apit.store.data_parser import extract_songs
from apit.store.download import download_artwork
from apit.store.download import download_metadata
from apit.store.download import generate_lookup_url
from apit.url_utils import is_url
from apit.user_input import ask_user_for_confirmation


def execute(
    files: list[Path],
    verbose_level: int,
    source: str,
    has_backup_flag: bool,
    has_embed_artwork_flag: bool,
    artwork_size: int,
) -> CommandResult:
    songs = to_songs(source)
    artwork = to_artwork(songs, artwork_size) if has_embed_artwork_flag else None

    actions: list[TagAction] = [
        create_action(file, songs, has_backup_flag, artwork) for file in files
    ]

    if any_action_needs_confirmation(actions):
        print_actions_preview(actions)
        ask_user_for_confirmation()

    for action in actions:
        logging.info("Executing: %s", action)
        action.apply()

    print_report(actions, TagActionReporter, verbose=verbose_level > 0)
    return (
        CommandResult.SUCCESS if all_actions_successful(actions) else CommandResult.FAIL
    )


def to_songs(source: str) -> list[Song]:
    metadata_json = get_metadata_json(source)
    return extract_songs(metadata_json)


def to_artwork(songs: list[Song], artwork_size: int) -> Artwork | None:
    if not songs:
        return None
    first_song = songs[0]  # TODO refactor # TODO fix possible IndexError

    size = artwork_size
    upscaled_url = upscale_artwork_url(first_song, size)
    logging.info("Use cover link (with size %d): %s", size, upscaled_url)
    logging.info("Download cover (with size %d) from: %s", size, upscaled_url)

    artwork_content, image_type = download_artwork(upscaled_url)
    return Artwork(content=artwork_content, mimetype=MimeType(image_type))


def create_action(
    file: Path, songs: list[Song], should_backup: bool, artwork: Artwork | None
) -> TagAction:
    disc, track = extract_disc_and_track_number(file)

    return TagAction(
        file,
        song=find_song(songs, disc=disc, track=track),
        should_backup=should_backup,
        artwork=artwork,
    )


def upscale_artwork_url(song: Song, size: int) -> str:
    return song.artwork_url.replace("100x100", f"{size}x{size}")


def get_metadata_json(source: str) -> str:
    logging.info("Input source: %s", source)
    if Path(source).exists():
        logging.info("Use downloaded metadata file: %s", source)
        try:
            return Path(source).read_text()
        except Exception:
            raise ApitError(f"Error while reading metadata file: {Path(source)}")
    elif is_url(source):
        logging.info("Use URL to download metadata: %s", source)
        query_url = generate_lookup_url(source)
        logging.info("Query URL: %s", query_url)
        return download_metadata(query_url)
    raise ApitError(f"Invalid input source: {source}")
