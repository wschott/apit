from argparse import RawDescriptionHelpFormatter

from ..common_cli_parser_arguments import add_path_argument
from ..common_cli_parser_arguments import add_verbose_argument
from .main import main


def setup_cli_parser(subparsers):
    show_command = subparsers.add_parser(
        "show",
        help="show metadata tags of files in PATH",
        formatter_class=RawDescriptionHelpFormatter,
        description="show metadata tags of files in PATH",
    )
    show_command.set_defaults(func=main)

    add_verbose_argument(show_command)
    add_path_argument(show_command)
