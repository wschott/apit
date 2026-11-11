from pathlib import Path

import pytest

from apit.core.errors import ApitError
from apit.infra.metadata_source.local_file_loader import LocalFileLoader


def test_load(tmp_path: Path, test_metadata: str):
    metadata_file = tmp_path / "metadata.json"
    metadata_file.write_text(test_metadata)

    assert LocalFileLoader().load(str(metadata_file)) == test_metadata


def test_load_with_invalid_source():
    with pytest.raises(ApitError, match="Invalid input source"):
        LocalFileLoader().load("does-not-exist.json")


def test_load_with_unreadable_file(tmp_path: Path):
    with pytest.raises(ApitError, match="Error while reading metadata file"):
        LocalFileLoader().load(str(tmp_path))
