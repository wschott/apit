from pathlib import Path
from typing import NamedTuple

import pytest

from apit.file_tags import FileTags
from apit.file_types.audio_file import AudioFile
from apit.metadata import Album
from apit.metadata import Artwork
from apit.metadata import Song
from apit.readable_names import ReadableTagName
from apit.store.data_parser import to_album
from apit.store.data_parser import to_song
from apit.tag_id import TagId
from apit.tagged_value import TaggedValue


class MockAction(NamedTuple):
    needs_confirmation: bool
    executed: bool
    successful: bool
    actionable: bool


class MockTagAction(NamedTuple):
    needs_confirmation: bool
    executed: bool
    successful: bool
    actionable: bool
    is_filename_identical_to_song: bool


class FakeTag(TaggedValue):
    def _get_readable_name(self, tag_id: TagId) -> ReadableTagName | None:
        if tag_id == TagId("known-tag"):
            return ReadableTagName.TITLE
        return None

    def value(self, verbose: bool) -> str:
        return self._unprocessed_value


class FakeFile(AudioFile):
    def __init__(self, file: Path) -> None:
        pass

    def read(self) -> FileTags:
        return test_file_tags_data

    def update(self, song: Song, artwork: Artwork | None = None) -> FileTags:
        return test_file_tags_data


test_file_tags_data = FileTags([FakeTag(TagId("tag_id"), "tag_value")])


@pytest.fixture
def make_tmp_file(tmp_path):
    def _make_tmp_file(name: str) -> Path:
        path_name: Path = tmp_path / name
        path_name.touch()
        return path_name

    return _make_tmp_file


@pytest.fixture()
def song_metadata_as_json_obj():
    return song_metadata_as_json_obj2(disc=2, track=3)


@pytest.fixture()
def album_metadata_as_json_obj():
    return album_metadata_as_json_obj2()


def song_metadata_as_json_obj2(disc, track):
    return [
        {
            "artistName": "Track Artist",
            "trackCensoredName": "Track (feat. Other & $Artist) [Bonus Track]",
            "collectionCensoredName": "Test Album Namè",
            "primaryGenreName": "Test Genré",
            "releaseDate": "2010-01-01T07:00:00Z",
            "trackNumber": track,
            "trackCount": 5,
            "discNumber": disc,
            "discCount": 3,
            "trackExplicitness": "explicit",
            "kind": "song",
            "trackId": 98765,
            "collectionId": 12345,
        },
        {
            "artistName": "Second Artist",
            "trackCensoredName": "Second Track",
            "collectionCensoredName": "Second Album",
            "primaryGenreName": "Second Genre",
            "releaseDate": "2010-01-01T07:00:00Z",
            "trackNumber": 10,
            "trackCount": 11,
            "discNumber": 12,
            "discCount": 13,
            "trackExplicitness": "explicit",
            "kind": "song",
            "trackId": 461746,
            "collectionId": 12345,
            "collectionArtistName": "Compilation Artist",  # TODO add test for this one
        },
    ]


def album_metadata_as_json_obj2():
    return [
        {
            "collectionType": "Album",
            "artistName": "Album Artist",
            "copyright": "℗ 2010 Album Copyright",
            "artworkUrl100": "cover-url",
        }
    ]


def dummy_album() -> Album:
    return to_album(album_metadata_as_json_obj2()[0])


def dummy_song(
    disc=1, track=1
) -> Song:  # TODO change disc/track number to something else
    return to_song(dummy_album(), song_metadata_as_json_obj2(disc=disc, track=track)[0])


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
def mock_action_is_filename_identical_to_song():
    return MockTagAction(None, None, None, True, True)


@pytest.fixture
def mock_action_actionable_not_is_filename_identical_to_song():
    return MockTagAction(None, None, None, True, False)


@pytest.fixture
def test_metadata() -> str:
    return Path("tests/fixtures/metadata.json").read_text()


@pytest.fixture
def test_album() -> Album:
    return dummy_album()


@pytest.fixture
def test_songs() -> list[Song]:
    return [
        dummy_song(),
    ]


@pytest.fixture
def test_song() -> Song:
    return dummy_song(disc=2, track=3)


@pytest.fixture
def test_file_tags() -> FileTags:
    return test_file_tags_data


def pytest_addoption(parser):
    parser.addoption(
        "--runintegration",
        action="store_true",
        default=False,
        help="run integration tests",
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


def assert_dummy_test_album(album):
    assert album.album_artist == "Album Artist"
    assert album.copyright == "℗ 2010 Album Copyright"
    assert album.artwork_url == "cover-url"


def assert_dummy_test_song(song):
    assert song.album_artist == "Album Artist"
    assert song.copyright == "℗ 2010 Album Copyright"
    assert song.collection_id == 12345
    assert song.artist == "Track Artist"
    assert song.album_name == "Test Album Namè"
    assert song.media_kind == "song"
    assert song.disc_number == 2
    assert song.disc_total == 3
    assert song.track_number == 3
    assert song.track_total == 5
    assert song.title == "Track (feat. Other & $Artist) [Bonus Track]"
    assert song.genre == "Test Genré"
    assert song.content_id == 98765
    assert song.rating == "explicit"
    assert song.release_date == "2010-01-01T07:00:00Z"
    assert not song.compilation
    assert song.artwork_url == "cover-url"
