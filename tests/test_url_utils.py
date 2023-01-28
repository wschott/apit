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
def test_valid_urls(url: str):
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
def test_invalid_urls(url: str):
    assert not is_url(url)
