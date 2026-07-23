"""Resumable server-side rendering."""

from __future__ import annotations

from typing import Any, Dict

from echoui.compiler.emit_web import _render_nodes


def render_ssr(lowered: Dict[str, Any]) -> str:
    html_body = _render_nodes(lowered["nodes"])
    resume = _resume_payload(lowered)
    return f'{html_body}<script type="application/json" id="__echoui_resume">{resume}</script>'


def _resume_payload(lowered: Dict[str, Any]) -> str:
    import json

    payload = {
        "app": lowered.get("app", {}),
        "click_map": lowered.get("click_map", {}),
        "hydrate": True,
    }
    return json.dumps(payload)
