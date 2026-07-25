"""EchoUI command-line interface."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

from echoui import __version__

_BUILD_TARGETS = ["web", "static", "tui", "desktop", "gui", "android", "ios"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="echoui", description="EchoUI build tool")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("version", help="Print version")

    new_p = sub.add_parser("new", help="Create a new EchoUI project")
    new_p.add_argument("name", nargs="?", default="my-app")

    dev_p = sub.add_parser("dev", help="Start dev server")
    dev_p.add_argument("--target", default="web")
    dev_p.add_argument("--port", type=int, default=7999)
    dev_p.add_argument("--host", default="0.0.0.0", help="Bind address (default 0.0.0.0)")
    dev_p.add_argument("entry", nargs="?", default="main.py")

    build_p = sub.add_parser("build", help="Build for target")
    build_p.add_argument("--target", default="web", choices=_BUILD_TARGETS)
    build_p.add_argument("--out", default=None)
    build_p.add_argument("--package", action="store_true", help="Package desktop/mobile artifact")
    build_p.add_argument("entry", nargs="?", default="main.py")

    preview_p = sub.add_parser("preview", help="Serve built dist")
    preview_p.add_argument("--port", type=int, default=8000)
    preview_p.add_argument("--dir", default="dist/web")

    export_p = sub.add_parser("export", help="Export static site")
    export_p.add_argument("--static", action="store_true")
    export_p.add_argument("entry", nargs="?", default="main.py")

    analyze_p = sub.add_parser("analyze", help="Print IR summary")
    analyze_p.add_argument("entry", nargs="?", default="main.py")

    check_p = sub.add_parser("check", help="Validate project structure and SSS tree")
    check_p.add_argument("entry", nargs="?", default="main.py")

    test_p = sub.add_parser("test", help="Run pytest suite")
    test_p.add_argument("pytest_args", nargs="*", default=[])

    sub.add_parser("doctor", help="Check toolchain and optional deps")

    add_p = sub.add_parser("add", help="Register a plugin module")
    add_p.add_argument("plugin", help="Plugin module path")

    args = parser.parse_args(argv)
    if args.cmd == "version" or args.cmd is None:
        print(f"echoui {__version__}")
        return 0
    if args.cmd == "new":
        return cmd_new(args.name)
    if args.cmd == "dev":
        return cmd_dev(args.entry, host=args.host, port=args.port, target=args.target)
    if args.cmd == "build":
        return cmd_build(args.entry, target=args.target, out=args.out, package=args.package)
    if args.cmd == "preview":
        return cmd_preview(port=args.port, directory=args.dir)
    if args.cmd == "export":
        return cmd_export(args.entry)
    if args.cmd == "analyze":
        return cmd_analyze(args.entry)
    if args.cmd == "check":
        return cmd_check(getattr(args, "entry", "main.py"))
    if args.cmd == "test":
        return cmd_test(args.pytest_args)
    if args.cmd == "doctor":
        return cmd_doctor()
    if args.cmd == "add":
        return cmd_add(args.plugin)
    parser.print_help()
    return 1


def cmd_new(name: str) -> int:
    root = Path(name)
    if root.exists():
        print(f"Directory exists: {name}")
        return 1
    root.mkdir()
    (root / "main.py").write_text(_COUNTER_TEMPLATE, encoding="utf-8")
    (root / "README.md").write_text(_NEW_README.format(name=name), encoding="utf-8")
    (root / ".gitignore").write_text(_NEW_GITIGNORE, encoding="utf-8")
    (root / "pyproject.toml").write_text(_NEW_PYPROJECT.format(name=name), encoding="utf-8")
    print(f"Created {name}/")
    print("  main.py  pyproject.toml  README.md  .gitignore")
    print(f"Next: cd {name} && pip install -e . && echoui build --target web && echoui dev --port 8765")
    return 0


def cmd_build(entry: str, *, target: str, out: str | None, package: bool = False) -> int:
    app = _load_app(entry)
    out_dir = out or f"dist/{target}"
    path = app.compile(target=target, out_dir=out_dir)
    if package and target == "desktop":
        pkg = _package_desktop(out_dir)
        if pkg:
            print(f"Packaged desktop -> {pkg}")
        else:
            print("package: pip install echoui[desktop] then re-run with --package")
    print(f"Built {target} -> {path}")
    return 0


def _package_desktop(out_dir: str) -> str | None:
    try:
        import PyInstaller.__main__ as pyi
    except ImportError:
        return None
    root = Path(out_dir)
    main_py = root / "main.py"
    if not main_py.exists():
        return None
    dist = root / "bundle"
    pyi.run(
        [
            str(main_py),
            "--onefile",
            "--name",
            "echoui-app",
            "--distpath",
            str(dist),
            "--workpath",
            str(root / "build"),
            "--specpath",
            str(root / "build"),
            "--noconfirm",
        ]
    )
    exe = dist / ("echoui-app.exe" if sys.platform.startswith("win") else "echoui-app")
    return str(exe) if exe.exists() else None


def cmd_dev(entry: str, *, host: str, port: int, target: str) -> int:
    app = _load_app(entry)
    dev_server(app, entry=entry, host=host, port=port)
    return 0


def cmd_preview(*, port: int, directory: str) -> int:
    import http.server
    import socketserver

    root = Path(directory)
    if not root.exists():
        print(f"Missing build output: {directory}")
        return 1

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, directory=str(root), **kwargs)

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Preview http://127.0.0.1:{port}")
        httpd.serve_forever()
    return 0


def cmd_export(entry: str) -> int:
    return cmd_build(entry, target="static", out=None, package=False)


def cmd_analyze(entry: str) -> int:
    app = _load_app(entry)
    ir = app.build_ir()
    screen = ir["screen"]
    nodes = _count_nodes(screen)
    print(f"screens: {len(app.screens)}")
    print(f"initial: {app.initial}")
    print(f"nodes: {nodes}")
    return 0


def cmd_check(entry: str | None = None) -> int:
    ok = True
    path = Path(entry) if entry else Path("main.py")
    if not path.exists():
        found = next(Path(".").glob("**/main.py"), None)
        path = found if found else path
    if not path.exists():
        print("Missing: main.py (run from project root or pass entry to build)")
        return 1
    try:
        from echoui.cli import _load_app
        from echoui.compiler.analyzer import analyze
        from echoui.compiler.parser import parse_app
        from echoui.compiler.sss import validate_sss_tree

        app = _load_app(str(path))
        parsed = parse_app(app)
        validate_sss_tree(parsed["root"])
        analyze(parsed)
        print(f"check: ok ({path}) — SSS valid")
    except Exception as exc:
        print(f"check: failed — {exc}")
        ok = False
    return 0 if ok else 1


def cmd_test(pytest_args: list[str]) -> int:
    cmd = [sys.executable, "-m", "pytest", "-q", *pytest_args]
    return subprocess.call(cmd)


def cmd_doctor() -> int:
    ok = True
    for mod, pip_extra in (
        ("aiohttp", "web"),
        ("textual", "tui"),
        ("PySide6", "desktop"),
    ):
        try:
            __import__(mod)
            print(f"  {mod}: ok")
        except ImportError:
            print(f"  {mod}: missing (pip install echoui[{pip_extra}])")
            ok = False
    print("doctor:", "ok" if ok else "some optional deps missing")
    return 0 if ok else 1


def cmd_add(plugin: str) -> int:
    import importlib

    mod = importlib.import_module(plugin)
    from echoui.plugin import setup_all

    if hasattr(mod, "register"):
        mod.register()
    setup_all()
    print(f"Loaded plugin: {plugin}")
    return 0


def _count_nodes(node: dict[str, Any]) -> int:
    total = 1
    for child in node.get("children", []):
        total += _count_nodes(child)
    return total


def _load_app(entry: str) -> Any:
    import importlib.util
    import sys

    path = Path(entry).resolve()
    entry_dir = str(path.parent)
    if entry_dir not in sys.path:
        sys.path.insert(0, entry_dir)
    spec = importlib.util.spec_from_file_location("echoui_entry", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {entry}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "app"):
        raise RuntimeError(f"{entry} must define `app`")
    return mod.app


def dev_server(app: Any, *, entry: str = "main.py", host: str = "0.0.0.0", port: int = 7999) -> None:
    """Serve compiled web assets with hot rebuild — no Python runtime for UI events."""
    import socket
    import sys
    import threading
    from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

    from watchfiles import watch

    out = Path("dist/web")
    entry_path = Path(entry).resolve()
    watch_dir = entry_path.parent

    def rebuild() -> None:
        app.compile(target="web", out_dir=str(out))

    rebuild()

    def watcher() -> None:
        for _changes in watch(watch_dir, raise_interrupt=False):
            try:
                rebuild()
                print("Rebuilt dist/web", file=sys.stderr, flush=True)
            except Exception as exc:
                print(f"Rebuild failed: {exc}", file=sys.stderr, flush=True)

    threading.Thread(target=watcher, daemon=True).start()

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, directory=str(out.resolve()), **kwargs)

        def log_message(self, fmt: str, *args: Any) -> None:
            if args and str(args[0]).startswith("GET /"):
                super().log_message(fmt, *args)

    bind = "127.0.0.1" if host == "0.0.0.0" else host
    httpd = ThreadingHTTPServer((bind, port), Handler)
    httpd.allow_reuse_address = True
    lan = ""
    try:
        lan = socket.gethostbyname(socket.gethostname())
    except OSError:
        lan = bind
    print("EchoUI dev (compile-local, static serve):", file=sys.stderr, flush=True)
    print(f"  local   http://127.0.0.1:{port}/", file=sys.stderr, flush=True)
    if host == "0.0.0.0" and lan not in ("127.0.0.1", "0.0.0.0", bind):
        print(f"  network http://{lan}:{port}/", file=sys.stderr, flush=True)
    print(f"  watching {watch_dir}", file=sys.stderr, flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


_COUNTER_TEMPLATE = '''from echoui import App, Screen, Store, col, text, button

class CounterStore(Store):
    count: int = 0

store = CounterStore()

class Counter(Screen):
    def build(self):
        return col(
            text(lambda: f"Count: {store.count}"),
            button("+1", on_click=lambda: setattr(store, "count", store.count + 1)),
        )

app = App(screens=[Counter], initial="Counter")
'''

_NEW_GITIGNORE = """dist/
__pycache__/
*.pyc
.venv/
.env
"""

_NEW_PYPROJECT = """[project]
name = "{name}"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "echoui[web]>=1.2.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""

_NEW_README = """# {name}

EchoUI app — install CLI then build like npm:

```bash
pip install echoui[web]
# or from this folder after cloning deps:
pip install -e .

echoui build --target web
echoui dev --port 8765
```

Open http://127.0.0.1:8765
"""


if __name__ == "__main__":
    raise SystemExit(main())
