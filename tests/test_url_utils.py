from apit.url_utils import is_url


def test_valid_urls():
    assert is_url("http://test-domain.com")
    assert is_url("https://test-domain.com")
    assert is_url("https://test-domain.com/path")
    assert is_url("http://test-domain.com/path?query")


def test_invalid_urls():
    assert not is_url("")
    assert not is_url("test-domain.com")
    assert not is_url("test-domain.com/path")
    assert not is_url("://test-domain.com/path?query")
