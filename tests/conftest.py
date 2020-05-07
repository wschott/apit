from pathlib import Path

import pytest


@pytest.fixture
def test_metadata():
    return Path('tests/fixtures/metadata.json').read_text()

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
