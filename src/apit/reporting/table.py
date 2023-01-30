from collections.abc import Iterable

from beautifultable import BeautifulTable
from beautifultable import WEP_WRAP

METADATA_TABLE_WIDTH = 122


def legend_table(rows: list[list[str]]) -> str:
    table = BeautifulTable(default_alignment=BeautifulTable.ALIGN_LEFT)
    table.set_style(BeautifulTable.STYLE_NONE)
    table.columns.separator = "→"

    for row in rows:
        table.rows.append(row)

    return str(table)


def tag_preview_table(header: list[str], rows: list[list[str]]) -> str:
    table = BeautifulTable(default_alignment=BeautifulTable.ALIGN_LEFT)
    table.set_style(BeautifulTable.STYLE_COMPACT)
    table.maxwidth = 126

    table.columns.header = header
    for row in rows:
        table.rows.append(row)

    table.columns.alignment[0] = BeautifulTable.ALIGN_CENTER
    table.columns.alignment[1] = BeautifulTable.ALIGN_CENTER
    return str(table)


def metadata_table(rows: Iterable[Iterable[str]], tag_length: int) -> str:
    table = BeautifulTable(
        default_alignment=BeautifulTable.ALIGN_LEFT, maxwidth=METADATA_TABLE_WIDTH
    )
    table.set_style(BeautifulTable.STYLE_NONE)
    table.columns.separator = "│"

    for row in rows:
        table.rows.append(row)

    table.columns.padding_left[0] = 0
    table.columns.padding_right[-1] = 0
    table.columns.width_exceed_policy = WEP_WRAP
    tag_column_width = 1 + tag_length  # +1 for padding
    table.columns.width = [
        tag_column_width,
        METADATA_TABLE_WIDTH - 1 - tag_column_width,
    ]  # -1 for separator (relevant for table max width)
    return str(table)
