from .show.cli_parser import setup_cli_parser as show_setup_cli_parser
from .tag.cli_parser import setup_cli_parser as tag_setup_cli_parser


def get_cli_parser_setups_fns():
    return [show_setup_cli_parser, tag_setup_cli_parser]
