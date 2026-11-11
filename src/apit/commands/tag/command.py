import logging
from collections.abc import Iterable
from collections.abc import Sequence
from pathlib import Path

from .action import TagAction
from apit.core.action import all_actions_successful
from apit.core.action import any_action_needs_confirmation
from apit.core.result import Result
from apit.core.errors import ApitError
from apit.core.metadata.artwork import Artwork
from apit.core.metadata.song import Song
from apit.core.metadata_parser import MetadataParser
from apit.core.track_matching import match
from apit.infra.cli.report import print_report
from apit.infra.cli.tag_preview import print_actions_preview
from apit.infra.cli.tag_reporter import TagActionReporter
from apit.infra.cli.user_input import confirm
from apit.infra.metadata_source.itunes_store_loader import ItunesStoreLoader
from apit.utils.mime_type import MimeType


def execute(
    files: Iterable[Path],
    verbose_level: int,
    should_backup: bool,
    should_embed_artwork: bool,
    artwork_size: int,
    metadata_json: str,
    metadata_parser: MetadataParser,
) -> Result:
    songs = metadata_parser.extract_songs(metadata_json)
    artwork = to_artwork(songs, artwork_size) if should_embed_artwork else None

    actions: list[TagAction] = [
        TagAction(m, should_backup, artwork) for m in match(files, songs)
    ]

    if any_action_needs_confirmation(actions):
        print_actions_preview(actions)
        if not confirm(prompt="Apply?", abort_text="Aborted."):
            raise ApitError("Aborted.")

    for action in actions:
        logging.info("Executing: %s", action)
        action.apply()

    print_report(actions, TagActionReporter, verbose=verbose_level > 0)
    return Result.SUCCESS if all_actions_successful(actions) else Result.FAIL


def to_artwork(songs: Sequence[Song], artwork_size: int) -> Artwork | None:
    if not songs:
        return None
    first_song = songs[0]  # TODO refactor # TODO fix possible IndexError

    url = first_song.album.artwork_url
    logging.info("Download cover (with size %d) from: %s", artwork_size, url)

    # TODO ItunesStore is used directly instead of a possible local file
    artwork_content, artwork_content_type = ItunesStoreLoader().download_artwork(
        url, artwork_size
    )
    try:
        mime_type = MimeType.from_content_type(artwork_content_type)
    except ValueError:
        raise ApitError(f"Unknown content type: {artwork_content_type}")
    return Artwork(content=artwork_content, mime_type=mime_type)
