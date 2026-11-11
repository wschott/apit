import pytest

from apit.core.errors import ApitError
from apit.infra.metadata_source.constants import StoreKind
from apit.infra.metadata_source.constants import StoreRating


def test_to_store_rating():
    assert StoreRating.from_rating_str("explicit") == StoreRating.EXPLICIT


def test_to_store_rating_for_invalid_str():
    with pytest.raises(ApitError, match="Unknown rating"):
        StoreRating.from_rating_str("invalid")


def test_to_store_kind():
    assert StoreKind.from_kind_str("song") == StoreKind.SONG


def test_to_store_kind_for_invalid_str():
    with pytest.raises(ApitError, match="Unknown kind"):
        StoreKind.from_kind_str("invalid")
