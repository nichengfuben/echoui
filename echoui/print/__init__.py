"""Print and PDF export helpers."""

from __future__ import annotations

from echoui.sprite import IRNode


def print_styles() -> str:
    return "@media print{body{background:#fff}.no-print{display:none}}"


def printable(node: IRNode) -> IRNode:
    node.props["data-printable"] = True
    return node


def page_break() -> IRNode:
    return IRNode("divider", props={"class": "page-break"})


def to_print_html(body: str, *, title: str = "Print") -> str:
    return f"""<!DOCTYPE html><html><head><title>{title}</title>
<style>{print_styles()}</style></head><body>{body}</body></html>"""
