from pathlib import Path
from typing import List


class Command:
    def execute(self, files: List[Path], options):
        raise NotImplementedError
