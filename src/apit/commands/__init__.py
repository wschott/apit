from apit.commands.command import Command
from apit.commands.list import ListCommand
from apit.commands.tag import TagCommand

__all__ = ["CommandFactory"]


commands: dict[str, type[Command]] = {
    "list": ListCommand,
    "tag": TagCommand,
}


class CommandFactory:
    @classmethod
    def get_cli_parser_setup_fns(cls):
        return [c.setup_cli_parser for c in commands.values()]
