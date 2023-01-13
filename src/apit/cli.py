import logging
import sys
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Sequence

from apit.cli_options import CliOptions
from apit.command_result import CommandResult
from apit.commands import get_cli_parser_setups_fns
from apit.defaults import FILE_FILTER
from apit.error import ApitError
from apit.exit_code import ExitCode
from apit.file_handling import collect_files
from apit.logging import configure_logging


def create_parser(command_cli_parser_setup_fns: Iterable[Callable]):
    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description="""
%(prog)s allows batch tagging .m4a file metadata tags using data from Apple Music/iTunes Store.

Execute %(prog)s <command> -h to show help for a specific command.

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
""",  # noqa: B950
    )
    command_subparsers = parser.add_subparsers(
        dest="command", title="commands", required=True
    )
    for parser_setup_fn in command_cli_parser_setup_fns:
        parser_setup_fn(command_subparsers)
    return parser


def parse_args(args: Sequence[str]) -> CliOptions:
    parser = create_parser(get_cli_parser_setups_fns())
    return parser.parse_args(args, namespace=CliOptions())


def _to_exit_code(command_result: CommandResult) -> ExitCode:
    return {
        CommandResult.SUCCESS: ExitCode.OK,
        CommandResult.FAIL: ExitCode.ERROR,
    }.get(command_result, ExitCode.ERROR)


def cli() -> None:
    try:
        options: CliOptions = parse_args(sys.argv[1:])
        sys.exit(_to_exit_code(main(options)))
    except ApitError as e:
        print(e, file=sys.stderr)
        sys.exit(ExitCode.USAGE_ERROR)


def main(options: CliOptions) -> CommandResult:
    configure_logging(_to_log_level(options.verbose_level))
    logging.info("CLI options: %s", options)

    files = collect_files(options.path, FILE_FILTER)
    if not files:
        raise ApitError("No matching files found")
    logging.info("Input path: %s", options.path)

    return options.func(files, options)


def _to_log_level(verbose_level: int) -> int:
    return {
        1: logging.INFO,
        2: logging.DEBUG,  # TODO not used anymore
    }.get(verbose_level, logging.WARN)
