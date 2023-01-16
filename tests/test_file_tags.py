from .conftest import TestTag
from apit.file_tags import FileTags
from apit.readable_names import ReadableTagName
from apit.tag_id import TagId


def test_file_tags_has_tags():
    file_tags = FileTags([TestTag(TagId("a"), "a-value")])

    assert file_tags.has_tags


def test_file_tags_are_empty():
    file_tags = FileTags([])

    assert not file_tags.has_tags


def test_file_tags_filter_known():
    known = TestTag(TagId("known-tag"), "known-tag-value")
    unknown = TestTag(TagId("unknown-tag"), "unknown-tag-value")

    file_tags = FileTags([known, unknown])

    assert file_tags.filter([ReadableTagName.TITLE]) == [known]


def test_file_tags_filter_unknown():
    known = TestTag(TagId("known-tag"), "known-tag-value")
    unknown = TestTag(TagId("unknown-tag"), "unknown-tag-value")

    file_tags = FileTags([known, unknown])

    assert file_tags.filter_unknown() == [unknown]
