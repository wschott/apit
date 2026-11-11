import shutil
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text()


# TODO change to use bak as the extension instead of filename suffix
def backup_file(file: Path) -> None:
    backup_file_path = file.with_stem(f"{file.stem}.bak")
    shutil.copy2(file, backup_file_path)
