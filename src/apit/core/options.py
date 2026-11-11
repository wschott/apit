from __future__ import annotations

from argparse import Namespace
from collections.abc import Callable
from collections.abc import Iterable
from pathlib import Path

from apit.core.result import Result


class Options(Namespace):
    func: Callable[[Iterable[Path], Options], Result]
    command: str
    verbose_level: int
    has_backup_flag: bool
    has_embed_artwork_flag: bool
    artwork_size: int
    path: Path
    source: str
