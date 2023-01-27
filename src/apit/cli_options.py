from __future__ import annotations

from argparse import Namespace
from collections.abc import Callable
from pathlib import Path

from apit.command_result import CommandResult


class CliOptions(Namespace):
    func: Callable[[list[Path], CliOptions], CommandResult]
    command: str
    verbose_level: int
    has_backup_flag: bool
    has_embed_artwork_flag: bool
    artwork_size: int
    path: Path
    source: str
