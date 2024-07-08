import logging
import sys
from argparse import ArgumentParser
from collections.abc import Callable

from apit.cli_options import CliOptions
from apit.command_result import CommandResult
from apit.commands import CommandFactory
from apit.errors import ApitError
from apit.exit_code import ExitCode
from apit.file_handling import collect_files
from apit.file_types import AudioFileFactory
from apit.logging import configure_logging


def create_parser(command_cli_parser_setup_fns: list[Callable]):
    parser = ArgumentParser(
        description="%(prog)s - music files tagging using Apple Music/iTunes Store metadata.",
        epilog="`%(prog)s <command> -h` shows help for a specific command.",
    )
    command_subparsers = parser.add_subparsers(
        dest="command", title="commands", required=True
    )
    for parser_setup_fn in command_cli_parser_setup_fns:
        parser_setup_fn(command_subparsers)
    return parser


def parse_args(args: list[str]) -> CliOptions:
    parser = create_parser(CommandFactory.get_cli_parser_setup_fns())
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
    # TODO options set up in commands to commands
    configure_logging(_to_log_level(options.verbose_level))
    logging.info("CLI options: %s", options)

    supported_extensions = AudioFileFactory.get_supported_extensions()
    files = collect_files(options.path, supported_extensions)
    if not files:
        raise ApitError(
            f"No matching files found (supported extensions: {', '.join(supported_extensions)})."
        )
    logging.info("Input path: %s", options.path)

    return options.func(files, options)


def _to_log_level(verbose_level: int) -> int:
    return {
        1: logging.INFO,
        2: logging.DEBUG,  # TODO not used anymore
    }.get(verbose_level, logging.WARN)
