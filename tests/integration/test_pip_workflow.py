"""Verify npm-like workflow: pip install wheel → echoui new → build."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_pip_install_wheel_then_echoui_cli(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    wheel = next(repo.glob("dist/echoui-1.0.0-py3-none-any.whl"), None)
    if wheel is None:
        subprocess.run([sys.executable, "-m", "build"], cwd=repo, check=True)
        wheel = next(repo.glob("dist/echoui-1.0.0-py3-none-any.whl"))

    venv = tmp_path / "venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    py = venv / "Scripts" / "python.exe"
    if not py.exists():
        py = venv / "bin" / "python"

    subprocess.run([str(py), "-m", "pip", "install", str(wheel), "-q"], check=True)
    ver = subprocess.run(
        [str(py), "-m", "echoui", "version"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "1.0.0" in ver.stdout

    app_dir = tmp_path / "demo-app"
    subprocess.run([str(py), "-m", "echoui", "new", str(app_dir)], check=True)
    assert (app_dir / "main.py").exists()
    assert (app_dir / "pyproject.toml").exists()

    subprocess.run(
        [str(py), "-m", "echoui", "build", "--target", "web", "main.py"],
        cwd=app_dir,
        check=True,
    )
    assert (app_dir / "dist" / "web" / "index.html").exists()
