from typing import List, Type

from apit.commands.base import Command
from apit.commands.show.command import ShowCommand
from apit.commands.tag.command import TagCommand
from apit.error import ApitError

AVAILABLE_COMMANDS: List[Type[Command]] = [
    ShowCommand,
    TagCommand,
]


def determine_command_type(command_name: str) -> Type[Command]:
    for CommandType in AVAILABLE_COMMANDS:
        if CommandType.COMMAND_NAME == command_name:
            return CommandType
    raise ApitError(f"Command '{command_name}' not found")
