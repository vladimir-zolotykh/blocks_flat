#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import Any
from dataclasses import dataclass, field
import re
import pprint

text = """
Item: Root
{
    Item: Child A
    {
        Item: Grandchild A1
        Item: Grandchild A2
        {
            Item: Great-Grandchild A2.1
        }
    }
    Item: Child B
}
"""

item_pattern = re.compile(r"^\s*Item:\s*(?P<name>[^\n]+)", re.MULTILINE)
block_pattern = re.compile(
    r"""
    (?P<item>^\s*Item:\s*[^\n]+)        # The item line
    (?:\s*\{                            # Optional open brace
    (?P<children>.*?)                   # Non-greedy match for children
    \})?                                # Optional closing brace
""",
    re.MULTILINE | re.DOTALL | re.VERBOSE,
)


@dataclass
class Item:
    name: str
    children: list[Item] = field(default_factory=list)


def parse_children(text: str) -> list[Item]:
    results: list[Item] = []
    if text:
        for match in block_pattern.finditer(text):
            item: Item | None = parse_item(match.group("item"))
            assert item
            results.append(item)
    return results


def parse_item(text: str) -> Item | None:
    item: Item | None
    children: list[Item] = []
    if text:
        block: re.Match[str] | None = block_pattern.match(text)
        assert block
        children = parse_children(block.group("children"))
        item_match = item_pattern.match(block.group("item"))
        assert item_match
        item = Item(name=item_match.group("name"), children=children)
    return item


if __name__ == "__main__":
    tree = parse_item(text)
    pprint.pprint(tree, width=100)
