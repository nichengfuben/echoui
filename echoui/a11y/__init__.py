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


def announce(message: str, *, polite: bool = True) -> Dict[str, str]:
    attrs = live_region(polite=polite)
    attrs["data-announce"] = message
    return attrs


def a11y_audit(root: IRNode) -> list[str]:
    """Rule-based a11y hints (not a WCAG certification)."""
    issues: list[str] = []
    interactive = {"button", "input", "link"}

    def walk(node: IRNode) -> None:
        props = node.props
        if node.role in interactive:
            if not props.get("aria-label") and not props.get("label") and not props.get("text"):
                issues.append(f"{node.id}: interactive role '{node.role}' missing label")
        if node.role == "image" and not props.get("alt"):
            issues.append(f"{node.id}: image missing alt text")
        for child in node.children:
            walk(child)

    walk(root)
    return issues
