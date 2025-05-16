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


class Block:
    def __init__(self, color: str, text: str, line_no: int = -1):
        self.color = color
        self.text = text
        self.line_no = line_no

    def __repr__(self):
        s: str = f"{self.color}: " if self.color else ""
        return s + f"{self.text}"


def next_block(sh: TextIO) -> Generator[Block, None, None]:
    for line_no, line in enumerate(sh, 1):
        sep = re.match(SEPARATOR_RE, line)
        if sep:
            continue            # skip "//"
        for blk in re.finditer(BLOCK_RE, line):
            blk_text = blk.group('body')
            body = re.match(BODY_RE, blk_text)
            if body:
                color, text = body.groups()
                yield Block(color, text, line_no=line_no)


if __name__ == '__main__':
    with io.StringIO(minion_blk) as sh:
        for block in next_block(sh):
            print(f"{block = }")
