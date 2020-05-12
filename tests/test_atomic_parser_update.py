from unittest.mock import call, patch

from apit.atomic_parser import (
    _generate_metadata_update_command,
    update_metadata,
)

ALBUM = {
    'artistName': 'Album Artist',
    'copyright': '℗ 2010 Album Copyright'
}

SONG = {
    'artistName': 'Main Artist',
    'trackCensoredName': 'Track (feat. Other & $Artist) [Bonus Track]',
    'collectionName': 'Album Namè',
    'primaryGenreName': 'Genre Namé',
    'releaseDate': '2010-01-30',
    'discNumber': 2,
    'discCount': 3,
    'trackNumber': 4,
    'trackCount': 5,
    'trackExplicitness': 'explicit',
    'kind': 'song',
    'trackId': 12345,
}

EXPECTED_GENERATED_COMMAND = [
    '--artist "Main Artist"',
    '--title "Track (feat. Other & $Artist) [Bonus Track]"',
    '--album "Album Namè"',
    '--genre "Genre Namé"',
    '--year "2010-01-30"',
    '--disknum 2/3',
    '--tracknum 4/5',
    '--advisory explicit',
    '--stik "Normal"',
    '--albumArtist "Album Artist"',
    '--copyright "℗ 2010 Album Copyright"',
    '--cnID "12345"',
]

EXPECTED_UPDATE_COMMAND = ' '.join(
    [
        '/Mock/AtomicParsley "dummy.m4a" --artist "Main Artist"',
        '--title "Track (feat. Other & \\$Artist) [Bonus Track]"',
        '--album "Album Namè" --genre "Genre Namé"',
        '--year "2010-01-30" --disknum 2/3 --tracknum 4/5',
        '--advisory explicit --stik "Normal"',
        '--albumArtist "Album Artist"',
        '--copyright "℗ 2010 Album Copyright"',
        '--cnID "12345"'
    ]
)


def test_generate_metadata_update_command():
    assert _generate_metadata_update_command(ALBUM, SONG, should_overwrite=False) == EXPECTED_GENERATED_COMMAND


@patch('apit.cmd._run_subprocess')
def test_metadata_updating(mock_run_subprocess, mock_atomicparsley_exe):
    _ = update_metadata('dummy.m4a', ALBUM, SONG, should_overwrite=False)
    assert mock_run_subprocess.call_args == call(EXPECTED_UPDATE_COMMAND, shell=True)


@patch('apit.cmd._run_subprocess')
def test_metadata_updating_with_overwriting(mock_run_subprocess, mock_atomicparsley_exe):
    _ = update_metadata('dummy.m4a', ALBUM, SONG, should_overwrite=True)
    assert mock_run_subprocess.call_args == call(EXPECTED_UPDATE_COMMAND + ' --overWrite', shell=True)
