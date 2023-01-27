from collections.abc import Callable
from itertools import chain
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


def flat_map(extract_fn: Callable[[T], list[R]], list_of_lists: list[T]) -> list[R]:
    flat_list: list[R] = []
    for inner_list in list_of_lists:
        flat_list.extend(extract_fn(inner_list))
    return flat_list


def flatten(lists: list[list[T]]) -> list[T]:
    return list(chain.from_iterable(lists))
