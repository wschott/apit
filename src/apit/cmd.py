import re
import subprocess
from pathlib import Path
from typing import List, Union

from apit.defaults import DEFAULT_AP_LOCATIONS
from apit.error import ApitError

REGEX_OUTER_QUOTE = re.compile(r'^(?P<start>[^\"]*\"{1})(?P<inner>.+)(?P<end>\"{1}[^\"]*)')


def execute_command(file: Path, command: Union[List[str], str], shell: bool = False) -> subprocess.CompletedProcess:
    shell_command = _generate_shell_command(_find_atomicparsley_executable(DEFAULT_AP_LOCATIONS), file, command, shell)
    return _run_subprocess(shell_command, shell=shell)


def _run_subprocess(shell_command: Union[List[str], str], shell: bool) -> subprocess.CompletedProcess:
    return subprocess.run(shell_command, shell=shell, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # TODO py3.7: return subprocess.run(shell_command, shell=shell, text=True, capture_output=True)


def _generate_shell_command(atomicparsley_executable: Path, file: Path, command: Union[List[str], str], shell: bool) -> Union[List[str], str]:
    command = _to_list(command)
    if shell:
        command = [str(atomicparsley_executable), _create_shell_friendly_filename(file)] + command
        command = [_escape_shell_arguments(c) for c in command]
        return ' '.join(command)
    else:
        return [str(atomicparsley_executable), str(file)] + command


def _to_list(command: Union[List[str], str]) -> List[str]:
    if isinstance(command, str):
        return [command]
    return command


def _find_atomicparsley_executable(locations) -> Path:
    for filename in locations:
        path = Path(filename).expanduser()
        if path.is_file():
            return path

    raise ApitError('AtomicParsley executable not found.')


def _create_shell_friendly_filename(file: Path) -> str:
    return f'"{file}"'


def _escape_shell_arguments(string: str) -> str:
    str_to_escape = string
    if str_to_escape.count('"') > 2:
        str_to_escape = _escape_inner_quotes(str_to_escape)

    return str_to_escape.replace('$', '\\$').replace('`', '\\`')


def _escape_inner_quotes(string: str) -> str:
    match = REGEX_OUTER_QUOTE.match(string)
    if not match:
        raise ApitError(f'An error occured while escaping: {string}')
    return ''.join([
        match.groupdict()['start'],
        match.groupdict()['inner'].replace('"', '\\"'),
        match.groupdict()['end'],
    ])
