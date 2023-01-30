from importlib.metadata import entry_points
from typing import Any


def load_entry_point_modules(group: str) -> dict[str, Any]:
    eps = entry_points(group=group)
    return {ep.name: ep.load() for ep in eps}
