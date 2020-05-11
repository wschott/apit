from unittest.mock import call, patch

from apit.atomic_parser import is_itunes_bought_file, read_metadata

EXPECTED_SHOW_COMMAND = ['/Mock/AtomicParsley', 'dummy.m4a', '-t']

def test_is_itunes_bought_file(monkeypatch):
    class MockCompletedProcess:
        def __init__(self, stdout):
            self.stdout = stdout
    monkeypatch.setattr('apit.atomic_parser.read_metadata', lambda *args: MockCompletedProcess('Atom "ownr" contains'))
    assert is_itunes_bought_file('tests/fixtures/1 itunes file.m4a')

def test_is_itunes_bought_file_not_itunes_file(monkeypatch):
    class MockCompletedProcess:
        def __init__(self, stdout):
            self.stdout = stdout
    monkeypatch.setattr('apit.atomic_parser.read_metadata', lambda *args: MockCompletedProcess('Atom "dummy" contains'))
    assert not is_itunes_bought_file('tests/fixtures/1 itunes file.m4a')

@patch('apit.cmd._run_subprocess')
def test_metadata_reading(mock_run_subprocess, mock_atomicparsley_exe):
    _ = read_metadata('dummy.m4a')
    assert mock_run_subprocess.call_args == call(EXPECTED_SHOW_COMMAND, shell=False)
