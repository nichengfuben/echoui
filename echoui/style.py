"""Compile-time style and theme helpers."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Optional


def style(**rules: Any) -> Dict[str, Any]:
    return dict(rules)


def css_hash(rules: Dict[str, Any]) -> str:
    raw = json.dumps(rules, sort_keys=True, default=str)
    return "e" + hashlib.md5(raw.encode()).hexdigest()[:8]


def rules_to_css(class_name: str, rules: Dict[str, Any]) -> str:
    parts = []
    for key, val in rules.items():
        if key in ("hover", "active", "focus", "dark", "media", "container"):
            continue
        prop = key.replace("_", "-")
        if isinstance(val, (list, tuple)):
            val = " ".join(str(v) for v in val)
        parts.append(f"{prop}:{val}")
    if not parts:
        return ""
    return f".{class_name}{{{';'.join(parts)};}}"


_theme: Dict[str, Any] = {
    "primary": "#6200EE",
    "surface": "#FFFFFF",
    "text": "#1A1A1A",
    "font_family": "system-ui, sans-serif",
}


def set_theme(**kwargs: Any) -> None:
    _theme.update(kwargs)


def theme(name: Optional[str] = None) -> Any:
    if name is None:
        return _ThemeProxy()
    return _theme.get(name, "")


def css(rules: str) -> str:
    """Global CSS escape (PLAN §8)."""
    return rules


def keyframes_css(name: str, frames: Dict[str, Dict[str, Any]]) -> str:
    parts = []
    for pct, rules in frames.items():
        body = ";".join(f"{k.replace('_', '-')}: {v}" for k, v in rules.items())
        parts.append(f"{pct} {{ {body}; }}")
    return f"@keyframes {name} {{ {' '.join(parts)} }}"


class _ThemeProxy:
    def __getattr__(self, item: str) -> Any:
        return _theme.get(item, "")

    def __getitem__(self, item: str) -> Any:
        return _theme[item]
