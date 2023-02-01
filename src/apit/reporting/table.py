from collections.abc import Iterable

from rich.table import box
from rich.table import Column
from rich.table import Table


def tag_preview_table(header: list[str | Column], rows: list[list[str]]) -> Table:
    table = Table(
        *header, box=box.SIMPLE, pad_edge=False, show_edge=False, collapse_padding=True
    )
    for row in rows:
        table.add_row(*row)
    return table


def metadata_table(
    known_rows: Iterable[Iterable[str]], unknown_rows: Iterable[Iterable[str]]
) -> Table:
    table = Table(box=box.MINIMAL, show_header=False, pad_edge=False, show_edge=False)
    for row in known_rows:
        table.add_row(*row)
    if known_rows and unknown_rows:
        table.add_section()
    for row in unknown_rows:
        table.add_row(*row)
    return table
