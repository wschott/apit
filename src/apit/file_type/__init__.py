from apit.file_type.audio_file import AudioFile
from apit.package_utils import import_packages

__all__ = ["AudioFile"]

import_packages(__path__)  # import formats in sub packages
