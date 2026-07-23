"""Reactive dependency analysis placeholder."""

from __future__ import annotations

from typing import Any, Dict


def analyze(parsed: Dict[str, Any]) -> Dict[str, Any]:
    parsed["signals"] = []
    root = parsed["root"]
    for node in _walk(root):
        for _k, binding in node.bindings.items():
            if isinstance(binding, dict) and binding.get("type") in ("signal", "computed", "fn"):
                parsed["signals"].append(binding)
    return parsed


def _walk(node: Any) -> Any:
    yield node
    for c in node.children:
        yield from _walk(c)
