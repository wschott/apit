from collections.abc import Mapping

from apit.command import Command
from apit.commands.show.command import ShowCommand
from apit.commands.tag.command import TagCommand
from apit.error import ApitError

AVAILABLE_COMMANDS: Mapping[str, type[Command]] = {
    "show": ShowCommand,
    "tag": TagCommand,
}


def determine_command_type(command_name: str) -> type[Command]:
    try:
        return AVAILABLE_COMMANDS[command_name]
    except KeyError:
        raise ApitError(f"Command '{command_name}' not found")
