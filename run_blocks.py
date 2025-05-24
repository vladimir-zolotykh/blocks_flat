#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> chart = make_chart(minion_blk)
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
import xml.etree.ElementTree as ET
from build_xml_tree import build_xml_tree
import block as BLK

BLOCK_RE = r"\[(?P<body>[^]]*)\]"
BODY_RE = r"(?:(?P<color>[^:]+):\s*)?(?P<text>[^]]+)"
SEPARATOR_RE = r"^/{1,2}$"

minion_blk = """\
[] [lightblue: Director]
//
[] [lightgreen: Secretary]
//
[Minion #1] [] [Minion #2]
"""

message_box_blk = """
[#00CCDE: MessageBox Window
    [lightgray: Frame
        [] [white: Message text]
        //
        [goldenrod: OK Button] [] [#ff0505: Cancel Button]
        /
        []
    ]
]
"""


def make_chart(fh: TextIO) -> BLK.Chart:
    chart: BLK.Chart = BLK.Chart()
    row_cur: int = 0
    for line_no, line in enumerate(fh, 1):
        row: BLK.Row = BLK.Row(row_cur)
        chart.add_row(row)
        if re.match(SEPARATOR_RE, line):
            row.add_node(BLK.Separator(line_no))
        else:
            for blk in re.finditer(BLOCK_RE, line):
                if body := re.match(BODY_RE, blk.group("body")):
                    color, text = body.groups()
                    color = color if color else "None"
                else:
                    color, text = "None", ""
                row.add_node(BLK.Block(color, text, line_no))
        row_cur += 1
    return chart


if __name__ == "__main__":
    # import doctest

    # doctest.testmod()
    with io.StringIO(message_box_blk) as fh:
        # chart: BLK.Chart = make_chart(fh)
        chart: BLK.Chart = make_chart(fh)
    import pprint

    pprint.pprint(chart)
    exit(0)
    svg: ET.Element = build_xml_tree(chart)
    tree = ET.ElementTree(svg)
    # filename: str = "run_blocks.svg"
    filename: str = "message_box.svg"
    with open(filename, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        f.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n')
        # fmt: off
        f.write(
            '    "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n'
        )
        # fmt: on
        tree.write(f, encoding="unicode")
