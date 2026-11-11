import logging

from apit.core.result import Result
from apit.core.errors import ApitError
from apit.core.options import Options
from apit.file_handling import collect_files
from apit.file_types import AudioFileFactory


def run(options: Options) -> Result:
    logging.info("Input path: %s", options.path)

    supported_extensions = AudioFileFactory.get_supported_extensions()
    files = collect_files(options.path, supported_extensions)
    if not files:
        raise ApitError(
            f"No matching files found (supported extensions: {', '.join(supported_extensions)})."
        )

    return options.func(files, options)
