from pathlib import Path

from apit.command.show import show_metadata
from apit.error import ApitError

BLACKLIST = [
    'Atom "ownr" contains',
    'Atom "apID" contains',
]

def is_itunes_bought_file(file: Path) -> bool:
    fileinfo = show_metadata(file)
    fileinfo = fileinfo.stdout

    if fileinfo is None:
        raise ApitError(f'AtomicParsley is not able to read the metadata of "{file}". Is this a valid .m4a file?')

    return any(map(lambda item: item in fileinfo, BLACKLIST))
