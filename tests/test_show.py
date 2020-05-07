from unittest.mock import call, patch

from apit.command.show import show_metadata

EXPECTED_SHOW_COMMAND = ['/Mock/AtomicParsley', 'dummy.m4a', '-t']

@patch('apit.cmd._run_subprocess')
def test_metadata_reading(mock_run_subprocess, mock_atomicparsley_exe):
    _ = show_metadata('dummy.m4a')
    assert mock_run_subprocess.call_args == call(EXPECTED_SHOW_COMMAND, shell=False)
