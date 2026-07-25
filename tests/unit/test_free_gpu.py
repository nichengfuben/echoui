"""GPU batching must not gray-out image layers in free-mode games."""

from echoui import Store
from echoui.compiler.analyzer import analyze
from echoui.compiler.client_cfg import build_client_cfg
from echoui.compiler.emit_free_gpu import collect_free_gpu
from echoui.compiler.lower import lower_web
from echoui.compiler.optimizer import optimize
from echoui.compiler.parser import parse_app
from echoui.compiler.ui_collect import analyze_ui


def test_free_gpu_skips_images():
    from pathlib import Path
    import importlib.util
    import sys

    root = Path(__file__).resolve().parents[2] / "examples" / "06_runner"
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location("runner", root / "main.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    Store.reset_registry()
    mod.RunnerStore()
    parsed = analyze(parse_app(mod.app))
    bindings, _, _, _ = analyze_ui(parsed["root"])
    gpu = collect_free_gpu(parsed["root"], bindings)
    assert gpu is not None
    colors = {n["c"] for n in gpu["nodes"]}
    assert "#888" not in colors
    assert "#87ceeb" in colors
    roles_with_bg = sum(1 for n in gpu["nodes"] if n["c"])
    assert roles_with_bg >= 3
