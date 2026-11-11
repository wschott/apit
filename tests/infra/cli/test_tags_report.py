from tests.conftest import fake_tag
from apit.core.audio.tag_name import TagName
from apit.infra.cli.tags_report import _filter_known
from apit.infra.cli.tags_report import _filter_unknown


def test_filter_known():
    known = fake_tag("known-tag", "known-tag-value")
    unknown = fake_tag("unknown-tag", "unknown-tag-value")

    assert _filter_known([known, unknown], [TagName.TITLE]) == [known]


def test_filter_known_follows_order_of_names():
    title = fake_tag("known-tag", "known-tag-value")

    assert _filter_known([title], [TagName.ARTIST, TagName.TITLE]) == [title]


def test_filter_unknown():
    known = fake_tag("known-tag", "known-tag-value")
    unknown = fake_tag("unknown-tag", "unknown-tag-value")

    assert _filter_unknown([known, unknown]) == [unknown]
