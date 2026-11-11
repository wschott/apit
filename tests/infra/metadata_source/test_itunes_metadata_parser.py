import pytest

from apit.core.errors import ApitError
from apit.core.metadata.media_kind import MediaKind
from apit.core.metadata.rating import Rating
from apit.core.metadata.disc_number import DiscNumber
from apit.core.metadata.track_number import TrackNumber
from apit.core.track_matching import find_song
from apit.infra.metadata_source.constants import StoreKey
from apit.infra.metadata_source.constants import StoreKind
from apit.infra.metadata_source.constants import StoreRating
from apit.infra.metadata_source.itunes_metadata_parser import _find_album
from apit.infra.metadata_source.itunes_metadata_parser import _find_songs
from apit.infra.metadata_source.itunes_metadata_parser import _extract_by_key
from apit.infra.metadata_source.itunes_metadata_parser import ItunesMetadataParser
from apit.infra.metadata_source.itunes_metadata_parser import to_album
from apit.infra.metadata_source.itunes_metadata_parser import to_media_kind
from apit.infra.metadata_source.itunes_metadata_parser import to_rating
from apit.infra.metadata_source.itunes_metadata_parser import to_song
from tests.conftest import assert_dummy_test_album
from tests.conftest import assert_dummy_test_song
from tests.conftest import dummy_album


def test_extract_songs(test_metadata):
    songs = ItunesMetadataParser().extract_songs(test_metadata)

    assert len(songs) == 14

    song = find_song(songs, disc=DiscNumber(1), track=TrackNumber(3))

    assert song is not None
    assert song.album_artist == "Kanye West"
    assert song.copyright == "℗ 2010 Roc-A-Fella Records, LLC"

    assert song.collection_id == 1440742903
    assert song.album_name == "My Beautiful Dark Twisted Fantasy"
    assert song.media_kind == MediaKind.SONG
    assert song.disc_number == 1
    assert song.track_number == 3
    assert song.title == "Power"


def test_extract_songs_using_invalid_metadata_with_format_error():
    with pytest.raises(ApitError, match="format error"):
        ItunesMetadataParser().extract_songs("")


@pytest.mark.parametrize(
    "json_str",
    [
        '{"test":[], "resultCount": 0}',
        '{"results":[], "test": 0}',
        '{"results":[], "resultCount": 0}',
    ],
)
def test_extract_songs_using_invalid_metadata_with_empty_results(json_str: str):
    with pytest.raises(ApitError, match="results empty"):
        ItunesMetadataParser().extract_songs(json_str)


def test_find_album(album_metadata_as_json_obj):
    album = _find_album(album_metadata_as_json_obj)

    assert_dummy_test_album(album)


def test_find_album_using_invalid_metadata():
    with pytest.raises(ApitError, match="No album found"):
        _find_album([])
    with pytest.raises(ApitError, match="No album found"):
        _find_album([{"collectionType": "Not Album"}])


def test_to_album(album_metadata_as_json_obj):
    album = to_album(album_metadata_as_json_obj[0])

    assert_dummy_test_album(album)


def test_to_album_using_invalid_metadata():
    with pytest.raises(ApitError):
        to_album({"invalid-key": "value"})


def test_find_songs(song_metadata_as_json_obj, test_album):
    songs = _find_songs(song_metadata_as_json_obj, test_album)

    assert len(songs) == 2

    song = find_song(songs, disc=DiscNumber(2), track=TrackNumber(3))
    assert_dummy_test_song(song)


def test_find_songs_using_invalid_metadata():
    test_album = dummy_album()

    assert _find_songs([], test_album) == []
    assert _find_songs([{"something": "not song"}], test_album) == []
    assert _find_songs([{"kind": "not song"}], test_album) == []


def test_to_song(song_metadata_as_json_obj, test_album):
    song = to_song(test_album, song_metadata_as_json_obj[0])

    assert_dummy_test_song(song)


def test_to_song_using_invalid_metadata(test_album):
    with pytest.raises(ApitError):
        to_song(test_album, {"invalid-key": "value"})


def test_extract_by_key():
    assert _extract_by_key(StoreKey.MEDIA_KIND, {"kind": "song"}) == "song"


def test_extract_by_key_using_invalid_metadata():
    with pytest.raises(ApitError, match="Unknown metadata key"):
        _extract_by_key("invalid-key", {"kind": "song"})  # type: ignore[ty:invalid-argument-type]
    with pytest.raises(ApitError, match="Metadata key not found"):
        _extract_by_key(StoreKey.MEDIA_KIND, {"invalid-key": "song"})


def test_to_rating():
    assert to_rating(StoreRating.EXPLICIT) == Rating.EXPLICIT


def test_to_rating_for_invalid_str():
    with pytest.raises(ApitError, match="Unknown rating"):
        to_rating("invalid")  # ty: ignore[invalid-argument-type]


def test_to_media_kind():
    assert to_media_kind(StoreKind.SONG) == MediaKind.SONG


def test_to_media_kind_for_invalid_str():
    with pytest.raises(ApitError, match="Unknown kind"):
        to_media_kind("invalid")  # ty: ignore[invalid-argument-type]
