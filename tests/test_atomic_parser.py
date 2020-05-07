from apit.atomic_parser import is_itunes_bought_file

EXPECTED_SHOW_COMMAND = ['/Mock/AtomicParsley', 'dummy.m4a', '-t']

def test_is_itunes_bought_file(monkeypatch):
    class MockResult:
        def __init__(self, stdout):
            self.stdout = stdout
    monkeypatch.setattr('apit.atomic_parser.show_metadata', lambda *args: MockResult('Atom "ownr" contains'))
    assert is_itunes_bought_file('tests/fixtures/1 itunes file.m4a')
