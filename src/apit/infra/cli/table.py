from collections.abc import Collection
from collections.abc import Iterable

from rich.table import box
from rich.table import Column
from rich.table import Table


def tag_preview_table(
    header: Iterable[str | Column], rows: Iterable[Iterable[str]]
) -> Table:
    table = Table(
        *header, box=box.SIMPLE, pad_edge=False, show_edge=False, collapse_padding=True
    )
    for row in rows:
        table.add_row(*row)
    return table


def metadata_table(
    known_rows: Collection[Iterable[str]], unknown_rows: Collection[Iterable[str]]
) -> Table:
    table = Table(box=box.MINIMAL, show_header=False, pad_edge=False, show_edge=False)
    known = list(known_rows)
    unknown = list(unknown_rows)
    for row in known:
        table.add_row(*row)
    if known and unknown:
        table.add_section()
    for row in unknown:
        table.add_row(*row)
    return table
