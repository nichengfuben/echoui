"""Resumable server-side rendering."""

from __future__ import annotations

from typing import Any, Dict

from echoui.compiler.client_cfg import cfg_json
from echoui.compiler.emit_web import _render_nodes


def render_ssr(lowered: Dict[str, Any]) -> str:
    html_body = _render_nodes(lowered["nodes"], gpu=lowered.get("free_gpu"))
    resume = cfg_json(lowered)
    return f'{html_body}<script type="application/json" id="__echoui_resume">{resume}</script>'
