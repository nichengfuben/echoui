"""Print and PDF export helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from echoui.sprite import IRNode


@dataclass
class PageStyle:
    """Print page box — maps to CSS @page."""

    size: str = "A4"
    margin: str = "2cm"
    orientation: str = "portrait"
    header: Optional[str] = None
    footer: Optional[str] = None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_css(self) -> str:
        orient = f" {self.orientation}" if self.orientation and self.orientation != "portrait" else ""
        parts = [f"size:{self.size}{orient}", f"margin:{self.margin}"]
        for k, v in self.extra.items():
            parts.append(f"{k.replace('_', '-')}:{v}")
        return f"@page{{{';'.join(parts)}}}"


def print_styles(*, page: PageStyle | None = None) -> str:
    base = "@media print{body{background:#fff}.no-print{display:none}.e-print-view{display:block}}"
    if page is None:
        return base
    return page.to_css() + base


def printable(node: IRNode) -> IRNode:
    node.props["data-printable"] = True
    return node


def page_break() -> IRNode:
    return IRNode("divider", props={"class": "page-break"})


def print_view(
    *children: Any,
    page: PageStyle | None = None,
    title: str = "Print",
    **extra: Any,
) -> IRNode:
    """IR region marked for print; optional PageStyle stored in props for emitters."""
    from echoui.sprite import normalize_children

    props: dict[str, Any] = {
        "role": "print_view",
        "class": "e-print-view",
        "title": title,
        **extra,
    }
    if page is not None:
        props["page_style"] = {
            "size": page.size,
            "margin": page.margin,
            "orientation": page.orientation,
            "header": page.header,
            "footer": page.footer,
            **page.extra,
        }
        props["page_css"] = page.to_css()
    return IRNode("box", props=props, children=normalize_children(list(children)))


def to_print_html(body: str, *, title: str = "Print", page: PageStyle | None = None) -> str:
    styles = print_styles(page=page)
    return f"""<!DOCTYPE html><html><head><title>{title}</title>
<style>{styles}</style></head><body>{body}</body></html>"""
