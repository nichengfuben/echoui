"""EchoUI per-target runtimes."""

from __future__ import annotations

from importlib import resources
from pathlib import Path

_WEB_PARTS = ("core.js", "storage.js", "webgpu.js", "widgets.js", "audio.js", "platform.js", "ui.js", "gestures.js")
RUNTIME_WEB_DIR = Path(__file__).parent / "web"


def _read_web_part(name: str) -> str:
    """Load runtime JS from package data (wheel) or source tree (editable)."""
    try:
        ref = resources.files("echoui.runtime").joinpath("web", name)
        if ref.is_file():
            return ref.read_text(encoding="utf-8")
    except (FileNotFoundError, ModuleNotFoundError, TypeError, OSError):
        pass
    path = RUNTIME_WEB_DIR / name
    if path.is_file():
        return path.read_text(encoding="utf-8")
    raise FileNotFoundError(
        f"Missing EchoUI web runtime asset: {name}. "
        f"Reinstall with: pip install --force-reinstall echoui[web]"
    )


def load_web_runtime(*, minify: bool = True) -> str:
    source = "\n".join(_read_web_part(name) for name in _WEB_PARTS)
    if not minify:
        return source
    try:
        import rjsmin

        return rjsmin.jsmin(source)
    except ImportError:
        return source
