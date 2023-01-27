from apit.package_utils import import_packages
from apit.tagging.audio_file import AudioFile

__all__ = ["AudioFile"]

import_packages(__path__)  # import formats in sub packages
