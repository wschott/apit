from pathlib import Path


class Command:
    def execute(self, files: list[Path], options):
        raise NotImplementedError
