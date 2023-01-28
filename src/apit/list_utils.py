from collections.abc import Iterable
from itertools import chain
from typing import TypeVar

T = TypeVar("T")


def flatten(lists: Iterable[Iterable[T]]) -> list[T]:
    return list(chain.from_iterable(lists))
