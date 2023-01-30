import pytest

from apit.errors import ApitError
from apit.mime_type import MimeType
from apit.mime_type import to_mime_type


def test_to_mime_type():
    assert to_mime_type("image/jpeg") == MimeType.JPEG
    assert to_mime_type("image/png") == MimeType.PNG


def test_to_mime_type_for_unknown_type():
    with pytest.raises(ApitError, match="Unknown content type: test-type"):
        to_mime_type("test-type")
