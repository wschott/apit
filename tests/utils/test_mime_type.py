import pytest

from apit.utils.mime_type import MimeType


@pytest.mark.parametrize(
    ("content_type", "mime_type"),
    [
        ("image/jpeg", MimeType.JPEG),
        ("image/png", MimeType.PNG),
    ],
)
def test_to_mime_type(content_type: str, mime_type: MimeType):
    assert MimeType.from_content_type(content_type) == mime_type


def test_to_mime_type_for_unknown_type():
    with pytest.raises(ValueError, match="Unknown content type: test-type"):
        MimeType.from_content_type("test-type")
