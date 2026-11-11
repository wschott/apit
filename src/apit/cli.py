import logging
import sys
from argparse import ArgumentParser
from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Sequence

from apit.core.app import run
from apit.core.options import Options
from apit.core.result import Result
from apit.commands import CommandFactory
from apit.core.errors import ApitError
from apit.infra.cli.exit_code import ExitCode
from apit.infra.cli.logger import ColoredFormatter


def create_parser(command_cli_parser_setup_fns: Iterable[Callable]):
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


def parse_args(args: Iterable[str]) -> Options:
    parser = create_parser(CommandFactory.get_cli_parser_setup_fns())
    return parser.parse_args(args, namespace=Options())


def _to_exit_code(result: Result) -> ExitCode:
    return {
        Result.SUCCESS: ExitCode.OK,
        Result.FAIL: ExitCode.ERROR,
    }.get(result, ExitCode.ERROR)


def cli() -> None:
    sys.exit(main(sys.argv[1:]))


def main(argv: Sequence[str]) -> ExitCode:
    try:
        options: Options = parse_args(argv)

        # TODO options set up in commands to commands
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColoredFormatter("%(levelname)s: %(message)s"))
        logging.basicConfig(
            level=_to_log_level(options.verbose_level), handlers=[console_handler]
        )
        logging.info("CLI options: %s", options)

        result = run(options)

        return _to_exit_code(result)
    except ApitError as e:
        print(e, file=sys.stderr)
        return ExitCode.USAGE_ERROR


def _to_log_level(verbose_level: int) -> int:
    return {
        1: logging.INFO,
        2: logging.DEBUG,  # TODO not used anymore
    }.get(verbose_level, logging.WARN)
