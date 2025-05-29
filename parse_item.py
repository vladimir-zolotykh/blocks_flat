#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import re

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


def parse_item(text, depth=0):
    matches = list(block_pattern.finditer(text))
    results = []
    for match in matches:
        name_match = item_pattern.search(match.group("item"))
        name = name_match.group("name") if name_match else "<Unknown>"
        children_text = match.group("children")
        children = parse_item(children_text, depth + 1) if children_text else []
        results.append({"name": name, "children": children})
    return results


if __name__ == "__main__":
    tree = parse_item(text)
    import pprint

    pprint.pprint(tree, width=100)
