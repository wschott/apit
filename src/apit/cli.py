import sys
from argparse import (
    ArgumentParser,
    ArgumentTypeError,
    RawDescriptionHelpFormatter,
)
from pathlib import Path
from typing import List

from apit.actions import AVAILAIBLE_ACTIONS
from apit.error import ApitError
from apit.main import main


def parse_args(args: List[str]):
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter, description="""
%(prog)s allows batch tagging .m4a file metadata tags using data from Apple Music/iTunes Store.

Filename format requirements
----------------------------
1. optional: disc number (followed by "-" or ".")
2. required: track number (followed by an optional ".")
3. required: ".m4a" extension

Examples:
  - without disc number (defaults to disc 1)
    - "14.m4a", "14 title.m4a", "14. title.m4a", "#14.m4a", "#14 title.m4a"
    - "2. 14 title.m4a" (track 2: title contains the number 14)
  - with disc number (e.g. disc 2)
    - "2-14 title.m4a", "2.14 title.m4a", "2.14. title.m4a"

Source requirement
------------------
one of the following:
- path to an existing file with already downloaded metadata
- URL to Apple Music/iTunes Store in order to download metadata
- album ID (with optional country code) of Apple Music/iTunes Store in order to download metadata
  - "us,123456789"
  - "123456789" (uses your system's locale for store determination)

URL format requirements
-----------------------
COUNTRY_CODE and ID required:
new style Apple Music: https://music.apple.com/{COUNTRY_CODE}/album/album-name/{ID}
or old style iTunes: http://itunes.apple.com/{COUNTRY_CODE}/album/album-name/id{ID}

Example:
  - https://music.apple.com/us/album/album-name/123456789
  - http://itunes.apple.com/us/album/album-name/id123456789
  - http://test-domain.com/us/test-name/42/123456789?i=09876
""")

    parser.add_argument(
        '-v', dest='verbose_level',
        action='count',
        help='increase verbosity of reporting (-vv prints debug messages)'
    )
    parser.add_argument(
        '-t', '--temp', dest='has_overwrite_flag',
        action='store_false', default=True,
        help='[only tag command] create temporary files with updated metadata (instead of overwriting files)'
    )
    parser.add_argument(
        '-c', '--cache', dest='has_search_result_cache_flag',
        action='store_true',
        help='[only tag command] save the downloaded metadata to disk'
    )
    parser.add_argument(
        'command', choices=[ActionType.COMMAND_NAME for ActionType in AVAILAIBLE_ACTIONS],
        help='available commands: "show" or "tag" metadata'
    )
    parser.add_argument(
        'path', metavar='PATH', type=_to_path,
        help='path containing m4a files'
    )
    parser.add_argument(
        'source', metavar='SOURCE', nargs='?',
        help='[only tag command] optional url (to be downloaded) or file (already downloaded) containing Apple Music/iTunes Store data or album ID (with optional country code)'
    )

    return parser.parse_args(args)


def _to_path(path_string: str) -> Path:
    path = Path(path_string).expanduser()

    if not path.is_dir():
        raise ArgumentTypeError(f'Invalid path: {path_string}')

    return path


def cli() -> None:
    try:
        options = parse_args(sys.argv[1:])
        sys.exit(main(options))
    except ApitError as e:
        print(e, file=sys.stderr)
        sys.exit(2)
