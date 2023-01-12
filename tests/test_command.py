from unittest.mock import patch

import pytest

from apit.command import Command


@patch.multiple(Command, __abstractmethods__=set())
def test_command_init():
    command = Command()

    with pytest.raises(NotImplementedError):
        command.execute([], {})
