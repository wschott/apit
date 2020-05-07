from pathlib import Path
from typing import List

from apit.cmd import execute_command_for_file
from apit.report import report_to_shell


def execute(files: List[Path], options):
    for file in files:
        report_to_shell(file, show_metadata(file))

def show_metadata(file: Path):
    command = ['-t']
    return execute_command_for_file(file, command)
