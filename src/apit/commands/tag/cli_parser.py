from argparse import RawDescriptionHelpFormatter

from ..common_cli_parser_arguments import add_path_argument
from ..common_cli_parser_arguments import add_verbose_argument
from .main import main


def setup_cli_parser(subparsers):
    tag_command = subparsers.add_parser(
        "tag",
        help="tag files in PATH",
        formatter_class=RawDescriptionHelpFormatter,
        description="""
tag files in PATH with metadata from Apple Music albums

SOURCE argument format
----------------------
one of:
- URL to Apple Music album for metadata download
- Apple Music style URLs: https://music.apple.com/<COUNTRY_CODE>/album/album-name/<ID>
  - Example: https://music.apple.com/us/album/album-name/123456789
- or iTunes style URLs: http://itunes.apple.com/<COUNTRY_CODE>/album/album-name/id<ID>
- path to a file with already downloaded metadata
""",
    )
    tag_command.set_defaults(func=main)

    add_verbose_argument(tag_command)
    tag_command.add_argument(
        "-b",
        "--backup",
        dest="has_backup_flag",
        action="store_true",
        default=False,
        help="create backup before updating tags (default: %(default)s)",
    )
    tag_command.add_argument(
        "-c",
        "--cache",
        dest="has_search_result_cache_flag",
        action="store_true",
        help="save the downloaded metadata to disk (default: %(default)s)",
    )
    tag_command.add_argument(
        "-a",
        "--artwork",
        dest="has_embed_artwork_flag",
        action="store_true",
        help="download artwork to disk and save in files (default: %(default)s)",
    )
    tag_command.add_argument(
        "--artwork-size",
        dest="artwork_size",
        metavar="SIZE",
        type=int,
        default=600,
        help="set artwork size for download (default: %(default)s)",
    )
    add_path_argument(tag_command)
    tag_command.add_argument(
        "source",
        metavar="SOURCE",
        help="URL to Apple Music album for metadata download OR file with already downloaded metadata",  # noqa: B950
    )
