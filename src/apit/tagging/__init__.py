from .format_registry import FormatRegistry
from .mp4 import Mp4Format

format_registry = FormatRegistry()
format_registry.register(Mp4Format)
