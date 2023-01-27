import pytest

from apit.error import ApitError
from apit.store.constants import StoreKind
from apit.store.constants import StoreRating
from apit.store.constants import to_item_kind
from apit.store.constants import to_rating


def test_to_rating():
    assert to_rating("explicit") == StoreRating.EXPLICIT


def test_to_rating_for_invalid_str():
    with pytest.raises(ApitError, match="Unknown rating"):
        to_rating("invalid")


def test_to_item_kind():
    assert to_item_kind("song") == StoreKind.SONG


def test_to_item_kind_for_invalid_str():
    with pytest.raises(ApitError, match="Unknown item kind"):
        to_item_kind("invalid")
