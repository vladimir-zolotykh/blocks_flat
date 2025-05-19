#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> chart = make_chart(minion_blk)
>>> import pprint
>>> pprint.pprint(chart)
[[Block(color=lightblue, text='Director', row=0, column=0, line_no=1)],
 [Separator(row=1, column=0, line_no=2)],
 [Block(color=lightgreen, text='Secretary', row=2, column=0, line_no=3)],
 [Separator(row=3, column=0, line_no=4)],
 [Block(color=None, text='Minion', row=4, column=0, line_no=5),
  Block(color=None, text='Minion', row=4, column=1, line_no=5)]]
"""

from typing import TextIO, Generator
import io
import re

BLOCK_RE = r"\[(?P<body>[^]]*)\]"
BODY_RE = r"(?:(?P<color>[^:]+):\s*)?(?P<text>\w+)"
SEPARATOR_RE = r"^/{1,2}$"

minion_blk = """\
[] [lightblue: Director]
//
[] [lightgreen: Secretary]
//
[Minion #1] [] [Minion #2]
"""


class Node:
    def __init__(self, row: int, column: int, line_no: int):
        self.row = row
        self.column = column
        self.line_no = line_no


class Row(list[Node]):
    def __init__(self, row: int) -> None:
        self.row = row

    def add_node(self, node: Node) -> None:
        self.append(node)


class Chart(list[Row]):
    def add_row(self, row: Row) -> None:
        self.append(row)


class Separator(Node):
    def __repr__(self):
        return (
            f"Separator(row={self.row}, column={self.column}, "
            f"line_no={self.line_no})"
        )


class Block(Node):
    def __init__(self, color: str, text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color
        self.text = text

    def __repr__(self):
        # s: str = f"{self.color}: " if self.color else ""
        # return s + f"{self.text}"
        return (
            f"Block(color={self.color}, text={self.text!r}, "
            f"row={self.row}, column={self.column}, "
            f"line_no={self.line_no})"
        )


def next_block(sh: TextIO) -> Generator[Node, None, None]:
    row: int = 0
    for line_no, line in enumerate(sh, 1):
        column: int = 0
        sep = re.match(SEPARATOR_RE, line)
        if sep:
            yield Separator(row, column, line_no)
        for blk in re.finditer(BLOCK_RE, line):
            blk_text = blk.group("body")
            body = re.match(BODY_RE, blk_text)
            if body:
                color, text = body.groups()
                yield Block(color, text, row, column, line_no)
                column += 1
        row += 1


def make_chart(input_str: str) -> Chart:
    with io.StringIO(minion_blk) as sh:
        chart: Chart = Chart()
        row_cur: int = 0
        row: Row = Row(row_cur)
        chart.add_row(row)
        for block in next_block(sh):
            if block.row == row.row:
                row.append(block)
            else:
                row_cur += 1
                row = Row(row_cur)
                chart.append(row)
                row.append(block)
        return chart


if __name__ == "__main__":
    import doctest

    doctest.testmod()
