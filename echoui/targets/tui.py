"""Textual TUI target — IR-driven widget tree."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator


def build_tui(app: Any, *, out_dir: str = "dist/tui") -> str:
    from echoui.compiler.analyzer import analyze
    from echoui.compiler.lower import lower_web
    from echoui.compiler.optimizer import optimize
    from echoui.compiler.parser import parse_app

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    parsed = parse_app(app)
    lowered = lower_web(optimize(analyze(parsed)))
    (out / "app.json").write_text(json.dumps(_sanitize_ir(lowered["nodes"]), indent=2), encoding="utf-8")
    (out / "main.py").write_text(_TUI_RUNNER, encoding="utf-8")
    return str(out.resolve())


def _sanitize_ir(node: Any) -> Any:
    """Strip callables from IR for JSON export."""
    if isinstance(node, list):
        return [_sanitize_ir(n) for n in node]
    if not isinstance(node, dict):
        return node
    clean: dict[str, Any] = {}
    for k, v in node.items():
        if k.startswith("_") or callable(v):
            continue
        if k == "props" and isinstance(v, dict):
            clean[k] = {pk: pv for pk, pv in v.items() if not callable(pv) and not pk.startswith("_")}
        elif isinstance(v, (dict, list)):
            clean[k] = _sanitize_ir(v)
        else:
            clean[k] = v
    return clean


def _text(props: dict[str, Any]) -> str:
    text = props.get("text", props.get("label", ""))
    return str(text) if not callable(text) else str(text())


def compose_ir(node: dict[str, Any]) -> Iterator[Any]:
    """Yield Textual widgets from lowered IR (import widgets lazily)."""
    from textual.containers import Horizontal, Vertical
    from textual.widgets import Button, Checkbox, Input, ProgressBar, Rule, Static

    role = node.get("role", "box")
    props = node.get("props", {})
    children = node.get("children", [])

    if role in ("text", "heading", "paragraph"):
        yield Static(_text(props))
        return
    if role == "button":
        yield Button(str(props.get("label", props.get("text", "Button"))))
        return
    if role == "divider":
        yield Rule()
        return
    if role in ("input", "textarea", "password", "number_input"):
        yield Input(placeholder=str(props.get("name", props.get("placeholder", "field"))))
        return
    if role == "checkbox" or role == "switch":
        yield Checkbox(str(props.get("label", props.get("text", "Option"))))
        return
    if role == "progress":
        yield ProgressBar(total=int(props.get("max", 100)), progress=int(props.get("value", 0)))
        return
    if props.get("direction") == "row" or role == "stage":
        with Horizontal():
            for child in children:
                yield from compose_ir(child)
        return
    if props.get("direction") == "col" or role in ("screen", "card", "box", "scroll"):
        with Vertical():
            for child in children:
                yield from compose_ir(child)
        return
    if children:
        with Vertical():
            for child in children:
                yield from compose_ir(child)
        return
    yield Static(_text(props) or role)


_TUI_RUNNER = '''"""Generated TUI runner — builds widgets from EchoUI IR."""
import json
from pathlib import Path

try:
    from textual.app import App, ComposeResult
except ImportError:
    raise SystemExit("pip install echoui[tui]")

from echoui.targets.tui import compose_ir


class EchoTuiApp(App):
    CSS = """
    Screen { padding: 1 2; }
    Button { margin: 1 0; }
    """

    def compose(self) -> ComposeResult:
        root = json.loads((Path(__file__).parent / "app.json").read_text(encoding="utf-8"))
        yield from compose_ir(root)


if __name__ == "__main__":
    EchoTuiApp().run()
'''
