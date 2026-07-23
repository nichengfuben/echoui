"""Accessibility helpers."""

from __future__ import annotations

from typing import Any, Dict

from echoui.sprite import IRNode


def aria(label: str, *, role: str | None = None, describedby: str | None = None) -> Dict[str, str]:
    attrs: Dict[str, str] = {"aria-label": label}
    if role:
        attrs["role"] = role
    if describedby:
        attrs["aria-describedby"] = describedby
    return attrs


def labelled(node: IRNode, label: str) -> IRNode:
    node.props.update(aria(label))
    return node


def focus_trap(enabled: bool = True) -> Dict[str, Any]:
    return {"data-focus-trap": enabled}


def skip_link(target: str, label: str = "Skip to content") -> IRNode:
    return IRNode("link", props={"href": target, "text": label, "class": "skip-link"})


def live_region(polite: bool = True) -> Dict[str, str]:
    return {"aria-live": "polite" if polite else "assertive"}
