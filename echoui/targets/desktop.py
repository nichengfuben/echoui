"""PySide6 desktop target."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from echoui.compiler.parser import parse_app


def build_desktop(app: Any, *, out_dir: str = "dist/desktop") -> str:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    parsed = parse_app(app)
    (out / "app.json").write_text(json.dumps(parsed["ir"], indent=2, default=str), encoding="utf-8")
    (out / "main.py").write_text(_DESKTOP_RUNNER, encoding="utf-8")
    return str(out.resolve())


def run_desktop(app_json: Path) -> None:
    try:
        from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
    except ImportError as e:
        raise ImportError("pip install echoui[desktop]") from e
    import sys

    qt = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("EchoUI Desktop")
    win.setCentralWidget(QLabel("EchoUI Desktop App"))
    win.resize(800, 600)
    win.show()
    sys.exit(qt.exec())


_DESKTOP_RUNNER = '''"""Generated desktop runner."""
import sys
from pathlib import Path
try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
except ImportError:
    raise SystemExit("pip install echoui[desktop]")

def main():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("EchoUI Desktop")
    win.setCentralWidget(QLabel("EchoUI Desktop"))
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
'''
