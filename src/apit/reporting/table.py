from collections.abc import Sequence

from beautifultable import BeautifulTable


def legend_table(rows: Sequence[Sequence[str]]) -> str:
    table = BeautifulTable(default_alignment=BeautifulTable.ALIGN_LEFT)
    table.set_style(BeautifulTable.STYLE_NONE)
    table.columns.separator = "→"
    for row in rows:
        table.rows.append(row)
    return str(table)


def tag_preview_table(header: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    table = _to_table(header, rows)
    table.maxwidth = 100
    table.columns.alignment[0] = BeautifulTable.ALIGN_CENTER
    return str(table)


def _to_table(header: Sequence[str], rows: Sequence[Sequence[str]]) -> BeautifulTable:
    table = BeautifulTable(default_alignment=BeautifulTable.ALIGN_LEFT)
    table.set_style(BeautifulTable.STYLE_COMPACT)
    table.columns.header = header
    for row in rows:
        table.rows.append(row)
    return table
