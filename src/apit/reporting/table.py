from collections.abc import Iterable

from beautifultable import BeautifulTable


def legend_table(rows: Iterable[Iterable[str]]) -> str:
    table = BeautifulTable(default_alignment=BeautifulTable.ALIGN_LEFT)
    table.set_style(BeautifulTable.STYLE_NONE)
    table.columns.separator = "→"
    for row in rows:
        table.rows.append(row)
    return str(table)


def tag_preview_table(header: Iterable[str], rows: Iterable[Iterable[str]]) -> str:
    table = _to_table(header, rows)
    table.maxwidth = 126
    table.columns.alignment[0] = BeautifulTable.ALIGN_CENTER
    table.columns.alignment[1] = BeautifulTable.ALIGN_CENTER
    return str(table)


def _to_table(header: Iterable[str], rows: Iterable[Iterable[str]]) -> BeautifulTable:
    table = BeautifulTable(default_alignment=BeautifulTable.ALIGN_LEFT)
    table.set_style(BeautifulTable.STYLE_COMPACT)
    table.columns.header = header
    for row in rows:
        table.rows.append(row)
    return table
