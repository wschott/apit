from apit.list_utils import flatten


def test_flatten_direct_elements():
    assert flatten([["a", "b"], ["c"]]) == ["a", "b", "c"]


def test_flatten_elements_with_properties():
    test_map = [{"prop": ["a", "b"]}, {"prop": ["c"]}]

    flat = flatten(x["prop"] for x in test_map)

    assert flat == ["a", "b", "c"]
