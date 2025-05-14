#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import TextIO, Generator
import io
import re

BLOCK_RE = r"\[(?P<block>[^]]+\]"
EMPTY_RE = r"^/{1,2}"
minion_blk = """\
[] [lightblue: Director]
//
[] [lightgreen: Secretary]
//
[Minion #1] [] [Minion #2]
"""


class Block:
    def __init__(self, line: str, line_no: int):
        self._line = line.rstrip()
        self._line_no = line_no

    def __repr__(self):
        return (f"{self._line_no}: {self._line}")


def next_block(sh: TextIO) -> Generator[Block, None, None]:
    for line_no, line in enumerate(sh, 1):
        yield Block(line, line_no)


if __name__ == '__main__':
    with io.StringIO(minion_blk) as sh:
        for block in next_block(sh):
            print(f"{block = }")
