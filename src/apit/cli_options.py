from __future__ import annotations

from argparse import Namespace
from pathlib import Path


class CliOptions(Namespace):
    command: str
    verbose_level: int
    has_backup_flag: bool
    has_search_result_cache_flag: bool
    has_embed_artwork_flag: bool
    artwork_size: int
    path: Path
    source: str | None
