#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import xml.etree.ElementTree as ET
import block as BLK


def build_xml_tree(chart: BLK.Chart, svg) -> ET.Element:
    svg = ET.Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "xmlns:xlink": "http://www.w3.org/1999/xlink",
            "xml:space": "preserve",
            "width": "432px",
            "height": "240px",
            "viewBox": "0 0 108 60",
        },
    )
    rect_width = 36
    rect_height = 10
    font_size = 5
    x_spacing = 36
    # y_spacing = 20
    # x_offset = 0
    y_offset = 10

    row: BLK.Row
    y: int = 0

    for row_index, row in enumerate(chart):
        x: int = 0
        node: BLK.Node
        for col_index, node in enumerate(row):
            x = col_index * x_spacing
            y = y_offset + row_index * (rect_height + 10)

            fill = node.color if node.color else "None"
            text = node.text
            ET.SubElement(
                svg,
                "rect",
                {
                    "x": str(x),
                    "y": str(y),
                    "width": str(rect_width),
                    "height": str(rect_height),
                    "fill": fill,
                    "stroke": "black",
                },
            )
            ET.SubElement(
                svg,
                "text",
                {
                    "x": str(x + rect_width // 2),
                    "y": str(y + rect_height - 3),
                    "text-anchor": "middle",
                    "font-size": str(font_size),
                },
            ).text = text

    return svg
