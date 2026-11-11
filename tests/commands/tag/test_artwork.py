from unittest.mock import patch

import pytest

from apit.core.errors import ApitError
from apit.commands.tag.command import to_artwork
from apit.infra.metadata_source.itunes_store_loader import ItunesStoreLoader

from tests.conftest import dummy_song


def test_to_artwork_with_unknown_content_type():
    with (
        patch.object(
            ItunesStoreLoader, "download_artwork", return_value=("content", "text/html")
        ),
        pytest.raises(ApitError, match="Unknown content type: text/html"),
    ):
        to_artwork([dummy_song()], artwork_size=600)
