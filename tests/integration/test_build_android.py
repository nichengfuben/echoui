"""Android Gradle project generation (+ APK when SDK present)."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

from echoui.compiler.bundler import build_target
from echoui.targets.android_gradle import build_android_gradle


def _load_hello():
    root = Path(__file__).resolve().parents[2] / "examples" / "01_hello_web"
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location("hi", root / "main.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.app


def test_build_android_web_assets(tmp_path):
    app = _load_hello()
    out = tmp_path / "android"
    path = build_target(app, target="android", out_dir=str(out))
    web = Path(path) / "assets" / "web" / "index.html"
    assert web.is_file()


def test_android_gradle_project_structure(tmp_path):
    app = _load_hello()
    base = tmp_path / "android"
    build_target(app, target="android", out_dir=str(base))
    project = Path(build_android_gradle(app, out_dir=str(base), sdk_root=str(tmp_path / "sdk")))
    assert (project / "app" / "build.gradle").is_file()
    assert (project / "gradlew.bat").is_file()
    assert (project / "app" / "src" / "main" / "java" / "com" / "echoui" / "app" / "MainActivity.java").is_file()


def test_android_assemble_debug_if_sdk():
    sdk = os.environ.get("ANDROID_SDK_ROOT") or os.environ.get("ANDROID_HOME")
    if not sdk or not Path(sdk).is_dir():
        pytest.skip("ANDROID_SDK_ROOT not set")
    app = _load_hello()
    base = Path(__file__).resolve().parents[2] / "dist" / "test-android-ci"
    if base.exists():
        import shutil

        shutil.rmtree(base, ignore_errors=True)
    build_target(app, target="android", out_dir=str(base))
    project = Path(build_android_gradle(app, out_dir=str(base), sdk_root=sdk))
    gradlew = project / "gradlew.bat" if sys.platform == "win32" else project / "gradlew"
    if not gradlew.is_file():
        pytest.skip("gradlew missing")
    subprocess.run(
        [str(gradlew), "assembleDebug", "--no-daemon"],
        cwd=project,
        check=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=600,
    )
    apk_dir = project / "app" / "build" / "outputs" / "apk" / "debug"
    apks = list(apk_dir.glob("*.apk"))
    assert apks, f"no apk in {apk_dir}"
