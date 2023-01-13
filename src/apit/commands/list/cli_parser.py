from argparse import RawDescriptionHelpFormatter

from ..common_cli_parser_arguments import add_path_argument
from ..common_cli_parser_arguments import add_verbose_argument
from .main import main


def setup_cli_parser(subparsers):
    list_command = subparsers.add_parser(
        "list",
        aliases=["ls"],
        help="list metadata tags of files in PATH",
        formatter_class=RawDescriptionHelpFormatter,
        description="list metadata tags of files in PATH",
    )
    list_command.set_defaults(func=main)

    add_verbose_argument(list_command)
    add_path_argument(list_command)
