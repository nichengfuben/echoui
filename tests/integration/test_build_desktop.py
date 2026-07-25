"""Desktop target + optional PyInstaller .exe packaging."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

from echoui.compiler.bundler import build_target


def _load_counter():
    root = Path(__file__).resolve().parents[2] / "examples" / "02_counter"
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location("ctr", root / "main.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.app


def test_build_desktop_writes_runner(tmp_path):
    app = _load_counter()
    out = tmp_path / "desktop"
    path = build_target(app, target="desktop", out_dir=str(out))
    assert Path(path).exists()
    assert (out / "main.py").exists()
    assert (out / "lowered.json").exists()


@pytest.mark.skipif(
    sys.platform != "win32",
    reason="PyInstaller onefile smoke test runs on Windows CI/dev",
)
def test_desktop_package_exe(tmp_path):
    pytest.importorskip("PyInstaller")
    from echoui.cli import _package_desktop

    app = _load_counter()
    out = tmp_path / "desktop"
    build_target(app, target="desktop", out_dir=str(out))
    exe = _package_desktop(str(out))
    assert exe is not None
    assert Path(exe).exists()
    assert Path(exe).suffix.lower() == ".exe"
