import pytest

from apit.utils.padded_number import padded_number


@pytest.mark.parametrize(
    ("number", "total", "expected"),
    [
        (3, 5, "3"),
        (3, 9, "3"),
        (3, 10, "03"),
        (3, 11, "03"),
        (3, 99, "03"),
        (3, 100, "003"),
        (10, 100, "010"),
        (100, 100, "100"),
        (1, 1, "1"),
        (0, 5, "0"),
        (5, 0, "5"),
    ],
)
def test_padded_number(number: int, total: int, expected: str):
    assert padded_number(number, total) == expected
