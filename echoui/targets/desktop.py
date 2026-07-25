"""PySide6 desktop target."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from echoui.compiler.analyzer import analyze
from echoui.compiler.lower import lower_web
from echoui.compiler.optimizer import optimize
from echoui.compiler.parser import parse_app


def build_desktop(app: Any, *, out_dir: str = "dist/desktop") -> str:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    parsed = parse_app(app)
    lowered = lower_web(optimize(analyze(parsed)))
    (out / "app.json").write_text(json.dumps(parsed["ir"], indent=2, default=str), encoding="utf-8")
    (out / "lowered.json").write_text(json.dumps(lowered["nodes"], indent=2, default=str), encoding="utf-8")
    (out / "main.py").write_text(_DESKTOP_RUNNER, encoding="utf-8")
    return str(out.resolve())


def run_desktop(app_json: Path) -> None:
    try:
        from PySide6.QtWidgets import QApplication, QMainWindow
    except ImportError as e:
        raise ImportError("pip install echoui[desktop]") from e
    import sys

    qt = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("EchoUI Desktop")
    lowered_path = app_json.parent / "lowered.json"
    if lowered_path.exists():
        from echoui.targets.desktop import render_qt_tree

        data = json.loads(lowered_path.read_text(encoding="utf-8"))
        central = render_qt_tree(data)
        win.setCentralWidget(central)
    else:
        from PySide6.QtWidgets import QLabel

        win.setCentralWidget(QLabel("EchoUI Desktop App"))
    win.resize(800, 600)
    win.show()
    sys.exit(qt.exec())


def render_qt_tree(node: dict[str, Any]) -> Any:
    try:
        from PySide6.QtWidgets import (
            QCheckBox,
            QHBoxLayout,
            QLabel,
            QLineEdit,
            QProgressBar,
            QPushButton,
            QVBoxLayout,
            QWidget,
        )
    except ImportError as e:
        raise ImportError("pip install echoui[desktop]") from e

    role = node.get("role", "box")
    props = node.get("props", {})
    children = node.get("children", [])

    if role in ("text", "heading", "paragraph"):
        return QLabel(str(props.get("text", props.get("label", ""))))
    if role == "button" or role == "icon_button":
        return QPushButton(str(props.get("label", props.get("text", "Button"))))
    if role in ("input", "textarea", "password", "number_input"):
        w = QLineEdit()
        w.setPlaceholderText(str(props.get("name", props.get("placeholder", ""))))
        if props.get("value"):
            w.setText(str(props["value"]))
        return w
    if role in ("checkbox", "switch"):
        cb = QCheckBox(str(props.get("label", props.get("text", "Option"))))
        if props.get("checked") or props.get("value"):
            cb.setChecked(True)
        return cb
    if role == "progress":
        bar = QProgressBar()
        bar.setMaximum(int(props.get("max", 100)))
        bar.setValue(int(props.get("value", 0)))
        return bar
    if props.get("direction") == "row" or role == "stage":
        box = QWidget()
        hlay = QHBoxLayout(box)
        for child in children:
            hlay.addWidget(render_qt_tree(child))
        return box
    box = QWidget()
    vlay = QVBoxLayout(box)
    for child in children:
        vlay.addWidget(render_qt_tree(child))
    return box


_DESKTOP_RUNNER = '''"""Generated desktop runner."""
import json
import sys
from pathlib import Path

try:
    from PySide6.QtWidgets import QApplication, QMainWindow
except ImportError:
    raise SystemExit("pip install echoui[desktop]")

from echoui.targets.desktop import render_qt_tree


def main():
    root = Path(__file__).parent
    data = json.loads((root / "lowered.json").read_text(encoding="utf-8"))
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("EchoUI Desktop")
    win.setCentralWidget(render_qt_tree(data))
    win.resize(900, 640)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
'''
