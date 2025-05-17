#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
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


class Token:
    def __init__(self, row: int, column: int, line_no: int):
        self.row = row
        self.column = column
        self.line_no = line_no


class Separator(Token):
    def __repr__(self):
        return (f"Separator(row={self.row}, column={self.column}, "
                f"line_no={self.line_no})")


class Block(Token):
    def __init__(self, color: str, text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color
        self.text = text

    def __repr__(self):
        # s: str = f"{self.color}: " if self.color else ""
        # return s + f"{self.text}"
        return (f"Block(color={self.color}, text={self.text!r}, "
                f"row={self.row}, column={self.column}, "
                f"line_no={self.line_no})")


def next_block(sh: TextIO) -> Generator[Token, None, None]:
    row: int = 0
    for line_no, line in enumerate(sh, 1):
        column: int = 0
        sep = re.match(SEPARATOR_RE, line)
        if sep:
            yield Separator(row, column, line_no)
        for blk in re.finditer(BLOCK_RE, line):
            blk_text = blk.group('body')
            body = re.match(BODY_RE, blk_text)
            if body:
                color, text = body.groups()
                yield Block(color, text, row, column, line_no)
                column += 1
        row += 1


if __name__ == '__main__':
    with io.StringIO(minion_blk) as sh:
        for block in next_block(sh):
            print(f"{block = }")
