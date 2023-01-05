from collections.abc import Callable
from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


def flat_map(
    extract_fn: Callable[[T], Iterable[R]], list_of_lists: Iterable[T]
) -> list[R]:
    flat_list: list[R] = []
    for inner_list in list_of_lists:
        flat_list.extend(extract_fn(inner_list))
    return flat_list
