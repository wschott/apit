from unittest.mock import call, patch

from apit.atomic_parser import (
    _generate_metadata_update_command,
    update_metadata,
)
from tests.conftest import dummy_song

SONG = dummy_song(disc=2, track=4)

EXPECTED_GENERATED_COMMAND = [
    '--artist "Track Artist"',
    '--title "Track (feat. Other & $Artist) [Bonus Track]"',
    '--album "Test Album Namè"',
    '--genre "Test Genré"',
    '--year "2010-01-01T07:00:00Z"',
    '--disknum 2/3',
    '--tracknum 4/5',
    '--advisory explicit',
    '--stik "Normal"',
    '--albumArtist "Album Artist"',
    '--copyright "℗ 2010 Album Copyright"',
    '--cnID "98765"',
]

EXPECTED_UPDATE_COMMAND = ' '.join(
    [
        '/Mock/AtomicParsley "dummy.m4a" --artist "Track Artist"',
        '--title "Track (feat. Other & \\$Artist) [Bonus Track]"',
        '--album "Test Album Namè" --genre "Test Genré"',
        '--year "2010-01-01T07:00:00Z" --disknum 2/3 --tracknum 4/5',
        '--advisory explicit --stik "Normal"',
        '--albumArtist "Album Artist"',
        '--copyright "℗ 2010 Album Copyright"',
        '--cnID "98765"'
    ]
)


def test_generate_metadata_update_command():
    assert _generate_metadata_update_command(SONG, should_overwrite=False) == EXPECTED_GENERATED_COMMAND


@patch('apit.cmd._run_subprocess')
def test_metadata_updating(mock_run_subprocess, mock_atomicparsley_exe):
    _ = update_metadata('dummy.m4a', SONG, should_overwrite=False)
    assert mock_run_subprocess.call_args == call(EXPECTED_UPDATE_COMMAND, shell=True)


@patch('apit.cmd._run_subprocess')
def test_metadata_updating_with_overwriting(mock_run_subprocess, mock_atomicparsley_exe):
    _ = update_metadata('dummy.m4a', SONG, should_overwrite=True)
    assert mock_run_subprocess.call_args == call(EXPECTED_UPDATE_COMMAND + ' --overWrite', shell=True)
