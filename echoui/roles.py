"""Role name to native tag registry."""

from __future__ import annotations

from typing import Any, Callable, Dict

ROLE_MAP: Dict[str, str] = {
    "text": "span",
    "heading": "h1",
    "paragraph": "p",
    "button": "button",
    "image": "img",
    "input": "input",
    "box": "div",
    "scroll": "div",
    "spacer": "div",
    "divider": "hr",
    "link": "a",
    "screen": "div",
    "stage": "div",
    "canvas": "canvas",
}

_custom_roles: Dict[str, Callable[..., Any]] = {}


def register_role(name: str, tag: str) -> None:
    ROLE_MAP[name] = tag


def role_tag(role: str) -> str:
    return ROLE_MAP.get(role, "div")


def register_role_renderer(name: str, renderer: Callable[..., Any]) -> None:
    _custom_roles[name] = renderer
