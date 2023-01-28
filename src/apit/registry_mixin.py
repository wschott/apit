from __future__ import annotations

import inspect
from typing import Generic
from typing import TypeVar

T = TypeVar("T")


class RegistryMixin(Generic[T]):
    registry: list[type[T]] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not inspect.isabstract(cls):
            cls.registry.append(cls)
