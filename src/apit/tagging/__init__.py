from .format_registry import FormatRegistry
from .mp3 import Mp3Format
from .mp4 import Mp4Format

format_registry = FormatRegistry()
format_registry.register(Mp4Format)
format_registry.register(Mp3Format)
