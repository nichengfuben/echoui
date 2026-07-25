"""Optimizer: static subtree marking and binding dedup."""

from __future__ import annotations

from typing import Any, Dict, List


def optimize(parsed: Dict[str, Any]) -> Dict[str, Any]:
    bindings: List[Dict[str, Any]] = parsed.get("reactive_bindings", [])
    seen: set[tuple[str, str]] = set()
    deduped: List[Dict[str, Any]] = []
    for b in bindings:
        key = (b.get("n", ""), b.get("t", ""))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(b)
    parsed["reactive_bindings"] = deduped
    parsed["optimized"] = True
    return parsed
