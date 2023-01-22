from __future__ import annotations

import inspect
from typing import Any


class RegistryMixin:
    registry: list[type[Any]] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not inspect.isabstract(cls):
            cls.registry.append(cls)
