from pathlib import Path

from apit.sort import sort_naturally


def test_sort_naturally_digits():
    _1 = Path("1. a.m4a")
    _3 = Path("3. c.m4a")
    _27 = Path("27. b.m4a")

    assert sort_naturally([_1, _27, _3]) == [_1, _3, _27]
