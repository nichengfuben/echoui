"""EchoUI command-line interface (PLAN §31)."""

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
    dev_p.add_argument("--host", default="127.0.0.1")
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

    sub.add_parser("check", help="Validate project structure")

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
        return cmd_check()
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
    print(f"Created {name}/main.py")
    return 0


def cmd_build(entry: str, *, target: str, out: str | None, package: bool = False) -> int:
    app = _load_app(entry)
    out_dir = out or f"dist/{target}"
    path = app.compile(target=target, out_dir=out_dir)
    if package and target == "desktop":
        print("package: use PyInstaller with dist/desktop (see docs/api/targets.md)")
    print(f"Built {target} -> {path}")
    return 0


def cmd_dev(entry: str, *, host: str, port: int, target: str) -> int:
    app = _load_app(entry)
    dev_server(app, host=host, port=port)
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


def cmd_check() -> int:
    ok = True
    if not Path("main.py").exists() and not any(Path(".").glob("**/main.py")):
        print("Missing: main.py (run from project root or pass entry to build)")
        ok = False
    if ok:
        print("check: ok")
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

    path = Path(entry).resolve()
    spec = importlib.util.spec_from_file_location("echoui_entry", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {entry}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "app"):
        raise RuntimeError(f"{entry} must define `app`")
    return mod.app


def dev_server(app: Any, host: str = "127.0.0.1", port: int = 7999) -> None:
    from aiohttp import web

    out = Path("dist/web")
    app.compile(target="web", out_dir=str(out))

    async def index(_req: web.Request) -> web.FileResponse:
        return web.FileResponse(out / "index.html")

    async def static_files(request: web.Request) -> web.FileResponse:
        return web.FileResponse(out / request.match_info["path"])

    async def action(request: web.Request) -> web.Response:
        body = await request.json()
        parsed = __import__("echoui.compiler.parser", fromlist=["parse_app"]).parse_app(app)
        handler = parsed["handlers"].get(body.get("handler", ""))
        if handler:
            handler()
            app.compile(target="web", out_dir=str(out))
        return web.json_response({"ok": True})

    srv = web.Application()
    srv.router.add_get("/", index)
    srv.router.add_post("/api/action", action)
    srv.router.add_get("/{path}", static_files)
    print(f"EchoUI dev server http://{host}:{port}")
    web.run_app(srv, host=host, port=port, print=None)


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


if __name__ == "__main__":
    raise SystemExit(main())
