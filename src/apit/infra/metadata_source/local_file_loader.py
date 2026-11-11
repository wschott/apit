import logging
from pathlib import Path
from typing import override

from apit.core.errors import ApitError
from apit.core.metadata_loader import MetadataLoader
from apit.utils.io import read_text


class LocalFileLoader(MetadataLoader):
    @override
    def load(self, source: str) -> str:
        path = Path(source)
        if not path.exists():
            raise ApitError(f"Invalid input source: {source}")

        logging.info("Use downloaded metadata file: %s", source)
        try:
            return read_text(path)
        except Exception:
            raise ApitError(f"Error while reading metadata file: {path}")
