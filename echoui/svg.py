"""SVG rendering helpers."""

from __future__ import annotations

from typing import Any, List

from echoui.sprite import IRNode


def svg_element(tag: str, **attrs: Any) -> str:
    parts = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    return f"<{tag} {parts}/>"


def svg_group(children: List[str], **attrs: Any) -> str:
    inner = "".join(children)
    parts = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    return f"<g {parts}>{inner}</g>"


def svg_doc(width: int, height: int, body: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">{body}</svg>'


def svg_node(width: int, height: int, body: str) -> IRNode:
    return IRNode("svg", props={"width": width, "height": height, "content": body})
