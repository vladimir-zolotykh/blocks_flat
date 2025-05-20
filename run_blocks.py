#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> chart = build_tree(minion_blk)
>>> import pprint
>>> pprint.pprint(chart)
[[Empty(line_no=1), Block(color=lightblue, text='Director', line_no=1)],
 [Separator(line_no=2)],
 [Empty(line_no=3), Block(color=lightgreen, text='Secretary', line_no=3)],
 [Separator(line_no=4)],
 [Block(color=None, text='Minion', line_no=5),
  Empty(line_no=5),
  Block(color=None, text='Minion', line_no=5)]]
"""

from typing import TextIO
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
    def __init__(self, line_no: int) -> None:
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
        return f"{self.__class__.__name__}(line_no={self.line_no})"


class Empty(Node):
    def __repr__(self):
        return f"{self.__class__.__name__}(line_no={self.line_no})"


class Block(Node):
    def __init__(self, color: str, text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color
        self.text = text

    def __repr__(self):
        # fmt: off
        return (
            f"{self.__class__.__name__}(color={self.color}, "
            f"text={self.text!r}, line_no={self.line_no})"
        )
        # fmt: on


def build_tree(sh: TextIO) -> Chart:
    chart: Chart = Chart()
    row_cur: int = 0
    with io.StringIO(minion_blk) as sh:
        for line_no, line in enumerate(sh, 1):
            row: Row = Row(row_cur)
            chart.add_row(row)
            sep = re.match(SEPARATOR_RE, line)
            if sep:
                row.add_node(Separator(line_no))
            else:
                for blk in re.finditer(BLOCK_RE, line):
                    blk_text = blk.group("body")
                    body = re.match(BODY_RE, blk_text)
                    if body:
                        color, text = body.groups()
                        row.add_node(Block(color, text, line_no))
                    else:
                        row.add_node(Empty(line_no))
            row_cur += 1
    return chart


if __name__ == "__main__":
    import doctest

    doctest.testmod()
