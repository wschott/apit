from apit.commands.command import Command
from apit.package_utils import load_entry_point_modules

__all__ = ["CommandFactory"]


commands: dict[str, Command] = load_entry_point_modules(group="apit.commands")


class CommandFactory:
    @classmethod
    def get_cli_parser_setup_fns(cls):
        return [c.setup_cli_parser for c in commands.values()]
