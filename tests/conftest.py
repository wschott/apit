from collections import namedtuple
from pathlib import Path

import pytest

from apit.metadata import Album, Song

MockAction = namedtuple('MockAction', ['needs_confirmation', 'executed', 'successful', 'actionable'])


@pytest.fixture
def mock_action_needs_confirmation():
    return MockAction(True, None, None, None)


@pytest.fixture
def mock_action_not_needs_confirmation():
    return MockAction(False, None, None, None)


@pytest.fixture
def mock_action_failed():
    return MockAction(None, True, False, None)


@pytest.fixture
def mock_action_success():
    return MockAction(None, True, True, None)


@pytest.fixture
def mock_action_not_executed():
    return MockAction(None, False, False, None)


@pytest.fixture
def mock_action_actionable():
    return MockAction(None, None, None, True)


@pytest.fixture
def mock_action_not_actionable():
    return MockAction(None, None, None, False)


@pytest.fixture
def test_metadata():
    return Path('tests/fixtures/metadata.json').read_text()


@pytest.fixture
def test_album():
    return Album({
        'collectionId': 12345,
        'artistName': 'Test Artist',
        'collectionName': 'Test Collection',
    })


@pytest.fixture
def test_song():
    return Song({
        'discNumber': 2,
        'trackNumber': 3,
    })


@pytest.fixture
def mock_atomicparsley_exe(monkeypatch):
    monkeypatch.setattr('apit.cmd._find_atomicparsley_executable', lambda *args: '/Mock/AtomicParsley')


def pytest_addoption(parser):
    parser.addoption(
        "--runintegration", action="store_true", default=False, help="run integration tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "integration: mark test as integration to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runintegration"):
        return
    skip_integration = pytest.mark.skip(reason="need --runintegration option to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)
