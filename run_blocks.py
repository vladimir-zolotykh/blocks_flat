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
import argparse
import argcomplete
import xml.etree.ElementTree as ET
from build_xml_tree import build_xml_tree
import block as BLK
import blk_input

BLOCK_RE = r"\[(?P<body>[^]]*)\]"
BODY_RE = r"(?:(?P<color>[^:]+):\s*)?(?P<text>[^]]+)"
SEPARATOR_RE = r"^/{1,2}$"


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


parser = argparse.ArgumentParser(
    description="Parse .blk file",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "blk_str",
    choices=[n for n in dir(blk_input) if not n.startswith("__")],
    help="Select .blk input to parse",
)
parser.add_argument("--print-chart", type=bool, help="Print Chart tree", default=False)

if __name__ == "__main__":
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    with io.StringIO(getattr(blk_input, args.blk_str)) as fh:
        chart: BLK.Chart = make_chart(fh)

    if args.print_chart:
        import pprint

        pprint.pprint(chart)
    svg: ET.Element = build_xml_tree(chart)
    tree = ET.ElementTree(svg)
    with open(f"{args.blk_str}.svg", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        f.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n')
        f.write('    "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
        tree.write(f, encoding="unicode")
