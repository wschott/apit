import pytest

from apit.command import Command


def test_command_init():
    command = Command()

    with pytest.raises(NotImplementedError):
        command.execute([], {})
