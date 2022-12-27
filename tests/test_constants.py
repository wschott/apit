import pytest

from apit.error import ApitError
from apit.store.constants import STORE_KIND
from apit.store.constants import STORE_RATING
from apit.store.constants import to_item_kind
from apit.store.constants import to_rating


def test_to_rating():
    assert to_rating("explicit") == STORE_RATING.EXPLICIT


def test_to_rating_for_invalid_str():
    with pytest.raises(ApitError, match="Unknown rating"):
        to_rating("invalid")


def test_to_item_kind():
    assert to_item_kind("song") == STORE_KIND.SONG


def test_to_item_kind_for_invalid_str():
    with pytest.raises(ApitError, match="Unknown item kind"):
        to_item_kind("invalid")
