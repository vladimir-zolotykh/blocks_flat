#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Node:
    abbreviated = True

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
        if self.abbreviated:
            return f"{self.__class__.__name__}()"
        return f"{self.__class__.__name__}(line_no={self.line_no})"


class Block(Node):
    def __init__(self, color: str, text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color
        self.text = text

    @property
    def is_empty(self):
        return self.color == "None" and self.text == ""

    def __repr__(self):
        if self.is_empty:
            return f"{self.__class__.__name__}()"
        if self.abbreviated:
            return f"{self.__class__.__name__}({self.color}, {self.text!r})"
        # fmt: off
        return (
            f"{self.__class__.__name__}(color={self.color}, "
            f"text={self.text!r}, line_no={self.line_no})"
        )
        # fmt: on
