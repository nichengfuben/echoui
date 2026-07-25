"""Verify npm-like workflow: pip install wheel → echoui new → build."""

from __future__ import annotations

import os
import subprocess
import sys
import tomllib
from pathlib import Path


def _run(cmd: list[str], *, env: dict[str, str] | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        check=True,
        env=env,
        cwd=str(cwd) if cwd else None,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _clean_env(base: dict[str, str] | None = None) -> dict[str, str]:
    env = dict(base or os.environ)
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        env.pop(key, None)
    env["NO_PROXY"] = "127.0.0.1,localhost"
    env["no_proxy"] = "127.0.0.1,localhost"
    return env


def _project_version(repo: Path) -> str:
    data = tomllib.loads((repo / "pyproject.toml").read_text(encoding="utf-8"))
    return str(data["project"]["version"])


def test_pip_install_wheel_then_echoui_cli(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    version = _project_version(repo)
    wheel = repo / "dist" / f"echoui-{version}-py3-none-any.whl"
    if not wheel.is_file():
        subprocess.run(
            [sys.executable, "-m", "build"],
            cwd=repo,
            check=True,
            env=_clean_env(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    assert wheel.is_file(), f"missing wheel: {wheel}"

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
        env=_clean_env(),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    env = _clean_env()
    env["PYTHONPATH"] = str(site) + os.pathsep + env.get("PYTHONPATH", "")

    ver = _run([sys.executable, "-m", "echoui", "version"], env=env)
    assert version in ver.stdout

    app_dir = tmp_path / "demo-app"
    _run([sys.executable, "-m", "echoui", "new", str(app_dir)], env=env)
    assert (app_dir / "main.py").exists()
    assert (app_dir / "pyproject.toml").exists()

    _run(
        [sys.executable, "-m", "echoui", "build", "--target", "web", "main.py"],
        env=env,
        cwd=app_dir,
    )
    assert (app_dir / "dist" / "web" / "index.html").exists()
    assert (app_dir / "dist" / "web" / "runtime.js").exists()
    runtime_js = (app_dir / "dist" / "web" / "runtime.js").read_text(encoding="utf-8")
    assert "loadFrameScript" in runtime_js
    core = site / "echoui" / "runtime" / "web" / "core.js"
    assert core.is_file(), f"missing packaged runtime asset: {core}"
