from collections.abc import Mapping
from collections.abc import Sequence
from typing import Any

import mutagen.mp4

from apit.action import Action
from apit.action import filter_errors
from apit.action import filter_not_actionable
from apit.action import filter_successes
from apit.commands.show.action import ReadAction
from apit.commands.show.reporter import ReadActionReporter
from apit.commands.tag.action import TagAction
from apit.commands.tag.reporter import TagActionReporter
from apit.error import ApitError
from apit.report_action import ActionReporter
from apit.reporting.color import Color
from apit.reporting.color import to_colored_text
from apit.store.constants import ITEM_KIND_MAPPING
from apit.store.constants import MP4_MAPPING
from apit.store.constants import RATING_MAPPING
from apit.store.constants import STORE_KIND
from apit.store.constants import STORE_RATING
from apit.string_utils import normalize_unicode
from apit.string_utils import truncate_text

FILENAME_TRUNCATION_LIMIT = 60
SEPARATOR_LENGTH = 80

TABLE_LINE_FORMAT = "[%s] %s  →  %s"
STR_SUCCESS = "✓"
STR_FAIL = "✘"

MP4_MAPPING_TO_HUMAN_READABLE: Mapping[MP4_MAPPING, str] = {
    MP4_MAPPING.TITLE: "Title",
    MP4_MAPPING.ARTIST: "Artist",
    MP4_MAPPING.TRACK_NUMBER: "Track #/Total",
    MP4_MAPPING.DISC_NUMBER: "Disc #/Total",
    MP4_MAPPING.GENRE: "Genre",
    MP4_MAPPING.RELEASE_DATE: "Date",
    MP4_MAPPING.ALBUM_NAME: "Album",
    MP4_MAPPING.ALBUM_ARTIST: "Album Artist",
    MP4_MAPPING.COMPOSER: "Composer",
    MP4_MAPPING.COPYRIGHT: "Copyright",
    MP4_MAPPING.COMPILATION: "Compilation?",
    MP4_MAPPING.GAPLESS: "Gapless?",
    MP4_MAPPING.RATING: "Rating",
    MP4_MAPPING.MEDIA_TYPE: "Media Type",
    MP4_MAPPING.CONTENT_ID: "Content ID",
    MP4_MAPPING.PLAYLIST_ID: "Playlist ID",
    MP4_MAPPING.ARTIST_ID: "Artist ID",
    MP4_MAPPING.GENRE_ID: "Genre ID",
    MP4_MAPPING.COMPOSER_ID: "Composer ID",
    MP4_MAPPING.ISRC_ID: "ISRC",
    MP4_MAPPING.GROUPING: "Grouping",
    MP4_MAPPING.COMMENT: "Comment",
    MP4_MAPPING.SORT_ORDER_TITLE: "Sort Title",
    MP4_MAPPING.SORT_ORDER_ARTIST: "Sort Artist",
    MP4_MAPPING.SORT_ORDER_ALBUM: "Sort Album",
    MP4_MAPPING.SORT_ORDER_ALBUM_ARTIST: "Sort Album Artist",
    MP4_MAPPING.ARTWORK: "Artwork",
    MP4_MAPPING.BPM: "BPM",
    MP4_MAPPING.TOOL: "Tool",
    MP4_MAPPING.LYRICS: "Lyrics",
    MP4_MAPPING.OWNER_NAME: "Owner",
    MP4_MAPPING.USER_MAIL: "Email",
    MP4_MAPPING.PURCHASE_DATE: "Purchase Date",
    MP4_MAPPING.STOREFRONT_ID: "Storefront ID",
}

RATING_TO_HUMAN_READABLE: Mapping[int, str] = {
    4: "<explicit (old value)>",  # TODO
    RATING_MAPPING[STORE_RATING.CLEAN]: "<clean>",
    RATING_MAPPING[STORE_RATING.EXPLICIT]: "<explicit>",
    RATING_MAPPING[STORE_RATING.NONE]: "<inoffensive>",
}

MEDIA_TYPE_TO_HUMAN_READABLE: Mapping[int, str] = {
    ITEM_KIND_MAPPING[STORE_KIND.SONG]: "<normal>",
}

ORDER_INFO_TRACK = [
    MP4_MAPPING.TITLE.value,
    MP4_MAPPING.SORT_ORDER_TITLE.value,
    MP4_MAPPING.ARTIST.value,
    MP4_MAPPING.SORT_ORDER_ARTIST.value,
    MP4_MAPPING.COMPOSER.value,
    MP4_MAPPING.TRACK_NUMBER.value,
    MP4_MAPPING.RATING.value,
    MP4_MAPPING.GAPLESS.value,
    MP4_MAPPING.BPM.value,
    MP4_MAPPING.MEDIA_TYPE.value,
]
ORDER_INFO_ALBUM = [
    MP4_MAPPING.ALBUM_NAME.value,
    MP4_MAPPING.SORT_ORDER_ALBUM.value,
    MP4_MAPPING.ALBUM_ARTIST.value,
    MP4_MAPPING.SORT_ORDER_ALBUM_ARTIST.value,
    MP4_MAPPING.DISC_NUMBER.value,
    MP4_MAPPING.COMPILATION.value,
    MP4_MAPPING.GENRE.value,
    MP4_MAPPING.RELEASE_DATE.value,
    MP4_MAPPING.COPYRIGHT.value,
]
ORDER_INFO_IDS = [
    MP4_MAPPING.CONTENT_ID.value,
    MP4_MAPPING.PLAYLIST_ID.value,
    MP4_MAPPING.ARTIST_ID.value,
    MP4_MAPPING.GENRE_ID.value,
    MP4_MAPPING.COMPOSER_ID.value,
    MP4_MAPPING.ISRC_ID.value,
]
ORDER_INFO_MISC = [
    MP4_MAPPING.TOOL.value,
    MP4_MAPPING.GROUPING.value,
    MP4_MAPPING.COMMENT.value,
    MP4_MAPPING.ARTWORK.value,
]
ORDER_INFO_USER = [
    MP4_MAPPING.OWNER_NAME.value,
    MP4_MAPPING.USER_MAIL.value,
    MP4_MAPPING.PURCHASE_DATE.value,
    MP4_MAPPING.STOREFRONT_ID.value,
]


def truncate_filename(text: str, length: int = FILENAME_TRUNCATION_LIMIT) -> str:
    return truncate_text(text, length)


def pad_with_spaces(string: str, length: int = FILENAME_TRUNCATION_LIMIT) -> str:
    return string.ljust(length, " ")


def separator() -> str:
    return "-" * SEPARATOR_LENGTH


def result_line(action: Action) -> str:
    text = TABLE_LINE_FORMAT % (
        _is_successful(action),
        pad_with_spaces(truncate_filename(normalize_unicode(action.file.name))),
        to_action_reporter(action).status_msg,
    )
    return to_colored_text(text=text, color=_to_color_for_result(action))


def _is_successful(action: Action) -> str:
    return STR_SUCCESS if action.successful else STR_FAIL


def _to_color_for_result(action: Action) -> Color:
    if not action.executed:
        return Color.YELLOW
    if not action.successful:
        return Color.RED
    return Color.GREEN


def print_report(actions: Sequence[Action]) -> None:
    successes = filter_successes(actions)
    if successes:
        print("\nProcess results:")
        for action in successes:
            print_processing_result(action)

    errors = filter_errors(actions)
    if errors:
        print("\nErrors during processing:")
        for action in errors:
            print_processing_result(action)

    skipped = filter_not_actionable(actions)

    print_summary(actions)
    print_summary_line(len(successes), len(errors), len(skipped))


def print_processing_result(action: Action) -> None:
    print(separator())
    print(result_line(action))
    print()
    if action.successful and isinstance(action.result, mutagen.mp4.MP4):
        print_tags(action.result)
    else:
        print(action.result)


def print_tags(mp4_file: mutagen.mp4.MP4) -> None:
    tags_to_print = accumulate_values_to_print(mp4_file)

    print("Track:")
    print("------")
    for tag in ORDER_INFO_TRACK:
        print_specific_tag(tag, tags_to_print.get(tag, None))
    print()
    print("Album:")
    print("------")
    for tag in ORDER_INFO_ALBUM:
        print_specific_tag(tag, tags_to_print.get(tag, None))
    print()
    print("IDs:")
    print("----")
    for tag in ORDER_INFO_IDS:
        print_specific_tag(tag, tags_to_print.get(tag, None))
    print()
    print("Misc:")
    print("-----")
    for tag in ORDER_INFO_MISC:
        print_specific_tag(tag, tags_to_print.get(tag, None))
    print()
    print("User:")
    print("-----")
    for tag in ORDER_INFO_USER:
        print_specific_tag(tag, tags_to_print.get(tag, None))
    print()
    print("Other:")
    print("-----")
    for k_v in sorted(tags_to_print.items()):
        tag, value = k_v
        if tag not in (
            ORDER_INFO_TRACK
            + ORDER_INFO_ALBUM
            + ORDER_INFO_IDS
            + ORDER_INFO_MISC
            + ORDER_INFO_USER
        ):
            print_specific_tag(tag, tags_to_print.get(tag, None))


def accumulate_values_to_print(mp4_file: mutagen.mp4.MP4) -> dict[str, Any]:
    if not mp4_file.tags:
        raise ApitError("No tags present")

    tags_to_print: dict[str, Any] = {}
    for tag, tag_value in mp4_file.tags.items():
        value_to_print = ""
        if isinstance(tag_value, list):
            for tag_list_value in tag_value:
                if tag == MP4_MAPPING.ARTWORK.value:
                    value_to_print += "<present>"
                elif tag in [
                    MP4_MAPPING.TRACK_NUMBER.value,
                    MP4_MAPPING.DISC_NUMBER.value,
                ]:
                    track = tag_list_value[0] or "<none>"
                    disc = tag_list_value[1] or "<none>"
                    value_to_print += f"{track}/{disc}"
                else:
                    value_to_print += str(tag_list_value)
        else:
            value_to_print += str(tag_value)

        tags_to_print[tag] = tags_to_print.get(tag, "") + value_to_print
    return tags_to_print


def print_specific_tag(key: str, value) -> None:
    if not value:
        return

    if key == MP4_MAPPING.RATING.value:
        print(
            get_tag_with_human_readable_description(key),
            RATING_TO_HUMAN_READABLE[int(value)],
        )
    elif key == MP4_MAPPING.MEDIA_TYPE.value:
        print(
            get_tag_with_human_readable_description(key),
            MEDIA_TYPE_TO_HUMAN_READABLE[int(value)],
        )
    elif key == MP4_MAPPING.LYRICS.value:
        print(
            get_tag_with_human_readable_description(key),
            "\n" + value.replace("\r", "\n"),
        )
    else:
        print(get_tag_with_human_readable_description(key), value)


def get_tag_with_human_readable_description(key) -> str:
    if is_known_mp4_mapping(key):
        new_key = MP4_MAPPING(key)
    else:
        new_key = key

    if new_key in MP4_MAPPING_TO_HUMAN_READABLE:
        return (
            f"{key} | "
            + pad_with_spaces(MP4_MAPPING_TO_HUMAN_READABLE.get(new_key, key), 13)
            + " |"
        )
    else:
        return pad_with_spaces(key, 13) + " |"


def is_known_mp4_mapping(key: str) -> bool:
    try:
        MP4_MAPPING(key)
    except ValueError:
        return False
    else:
        return True


def print_summary(actions: Sequence[Action]) -> None:
    print("\nSummary:")
    print(separator())
    for action in actions:
        print(result_line(action))


def print_summary_line(successes: int, errors: int, skipped: int) -> None:
    summary = []
    if successes:
        summary.append(to_colored_text(f"{successes} processed", Color.GREEN))
    if errors:
        summary.append(to_colored_text(f"{errors} failed", Color.RED))
    if skipped:
        summary.append(to_colored_text(f"{skipped} skipped", Color.YELLOW))

    bar_color = Color.GREEN
    if errors:
        bar_color = Color.RED
    elif skipped:
        bar_color = Color.YELLOW

    summary_text = f" {', '.join(summary)} "
    print(
        "\n"
        + to_colored_text("=" * 30, bar_color)
        + summary_text
        + to_colored_text("=" * 30, bar_color)
    )


def to_action_reporter(action: Action) -> ActionReporter:
    if isinstance(action, ReadAction):
        return ReadActionReporter(action)
    elif isinstance(action, TagAction):
        return TagActionReporter(action)
    raise ApitError("Unknown action")
