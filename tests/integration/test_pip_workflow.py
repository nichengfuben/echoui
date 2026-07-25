"""Verify npm-like workflow: pip install wheel → echoui new → build."""

from __future__ import annotations

import os
import subprocess
import sys
import tomllib
from pathlib import Path


def _project_version(repo: Path) -> str:
    data = tomllib.loads((repo / "pyproject.toml").read_text(encoding="utf-8"))
    return str(data["project"]["version"])


def test_pip_install_wheel_then_echoui_cli(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    version = _project_version(repo)
    subprocess.run([sys.executable, "-m", "build"], cwd=repo, check=True)
    wheel = next(repo.glob(f"dist/echoui-{version}-py3-none-any.whl"))

    site = tmp_path / "site"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            str(wheel),
            "-q",
            "--target",
            str(site),
            "--no-deps",
        ],
        check=True,
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(site) + os.pathsep + env.get("PYTHONPATH", "")

    ver = subprocess.run(
        [sys.executable, "-m", "echoui", "version"],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    assert version in ver.stdout

    app_dir = tmp_path / "demo-app"
    subprocess.run(
        [sys.executable, "-m", "echoui", "new", str(app_dir)],
        check=True,
        env=env,
    )
    assert (app_dir / "main.py").exists()
    assert (app_dir / "pyproject.toml").exists()

    subprocess.run(
        [sys.executable, "-m", "echoui", "build", "--target", "web", "main.py"],
        cwd=app_dir,
        check=True,
        env=env,
    )
    assert (app_dir / "dist" / "web" / "index.html").exists()
    assert (app_dir / "dist" / "web" / "runtime.js").exists()
    runtime_js = (app_dir / "dist" / "web" / "runtime.js").read_text(encoding="utf-8")
    assert "loadFrameScript" in runtime_js
    core = site / "echoui" / "runtime" / "web" / "core.js"
    assert core.is_file(), f"missing packaged runtime asset: {core}"
