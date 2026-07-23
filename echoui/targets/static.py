"""Static site generation target."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from echoui.compiler.analyzer import analyze
from echoui.compiler.emit_web import _render_nodes, emit_web
from echoui.compiler.lower import lower_web
from echoui.compiler.optimizer import optimize
from echoui.compiler.parser import parse_app


def build_static(app: Any, *, out_dir: str = "dist/static") -> str:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    screens = list(app.screens.keys())
    for name in screens:
        app.switch_screen(name)
        parsed = parse_app(app)
        analyzed = analyze(parsed)
        optimized = optimize(analyzed)
        lowered = lower_web(optimized)
        html_body = _render_nodes(lowered["nodes"])
        files = emit_web(lowered, ssr_html=html_body)
        fname = "index.html" if name == app.initial else f"{name.lower()}.html"
        (out / fname).write_text(files["index.html"], encoding="utf-8")
    (out / "screens.json").write_text(json.dumps(screens), encoding="utf-8")
    return str(out.resolve())
