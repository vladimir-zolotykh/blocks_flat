#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
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


if __name__ == '__main__':
    with io.StringIO(minion_blk) as sh:
        for line_no, line in enumerate(sh, 1):
            print(f"{line_no = }, {line = }")
