import pytest

from apit.url_utils import is_url


@pytest.mark.parametrize(
    "url",
    [
        "http://test-domain.com",
        "https://test-domain.com",
        "https://test-domain.com/path",
        "http://test-domain.com/path?query",
    ],
)
def test_is_url_for_valid_url(url: str):
    assert is_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "",
        "test-domain.com",
        "test-domain.com/path",
        "://test-domain.com/path?query",
    ],
)
def test_is_url_for_invalid_url(url: str):
    assert not is_url(url)
