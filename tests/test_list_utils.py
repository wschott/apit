from apit.list_utils import flat_map
from apit.list_utils import flatten


def test_direct_elements():
    test_map = [["a", "b"], ["c"]]

    flat = flat_map(lambda x: x, test_map)

    assert flat == ["a", "b", "c"]


def test_elements_with_properties():
    test_map = [{"prop": ["a", "b"]}, {"prop": ["c"]}]

    flat = flat_map(lambda x: x["prop"], test_map)

    assert flat == ["a", "b", "c"]


def test_flatten_direct_elements():
    assert flatten([["a", "b"], ["c"]]) == ["a", "b", "c"]
