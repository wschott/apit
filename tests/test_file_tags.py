from .conftest import fake_tag
from apit.core.audio.file_tags import FileTags


def test_file_tags_has_tags():
    file_tags = FileTags([fake_tag("a", "a-value")])

    assert file_tags.has_tags


def test_file_tags_are_empty():
    file_tags = FileTags([])

    assert not file_tags.has_tags


def test_file_tags_tags():
    first = fake_tag("a", "a-value")
    second = fake_tag("b", "b-value")

    assert FileTags([first, second]).tags == (first, second)
