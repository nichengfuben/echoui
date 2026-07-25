"""Verify every UI handler compiles to local JS (PLAN §34: compile, don't interpret)."""

from __future__ import annotations

from typing import Any, Callable, Dict, List

from echoui.exceptions import CompileError


def validate_local_compile(parsed: Dict[str, Any]) -> None:
    """Fail the build if any non-frame handler lacks a local compiled action."""
    frame_hids = {item["handler"] for item in parsed.get("frame_handlers", [])}
    actions: Dict[str, Any] = parsed.get("actions", {})
    handlers: Dict[str, Callable[..., Any]] = parsed.get("handlers", {})
    errors: List[str] = []

    if frame_hids and not parsed.get("frame_script"):
        errors.append("frame handlers present but frame_script did not compile")

    for hid, fn in handlers.items():
        if hid in frame_hids:
            continue
        action = actions.get(hid)
        if action and action.get("local"):
            continue
        qual = getattr(fn, "__qualname__", repr(fn))
        errors.append(f"{qual} ({hid})")

    if errors:
        joined = "; ".join(errors)
        raise CompileError(
            "Handlers must compile to local client JS at build time — "
            f"not compiled: {joined}. "
            "Use Store mutations, module-level game functions, or @on('frame') for loops."
        )
