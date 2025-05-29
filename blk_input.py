#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

minion_blk = """\
[] [lightblue: Director]
//
[] [lightgreen: Secretary]
//
[Minion #1] [] [Minion #2]
"""

minion_blk_experimental = """\
[] [#00CCDE: Director]
//
[] [lightgreen: Secretary]
//
[Minion #1] [] [Minion #2]
"""

message_simple = """\
[#00CCDE: MessageBox Window
]
"""

message_box_blk = """\
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
