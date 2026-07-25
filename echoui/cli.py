"""EchoUI command-line interface."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from echoui import __version__


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
    build_p.add_argument("--target", default="web", choices=["web", "static", "tui", "desktop", "gui"])
    build_p.add_argument("--out", default=None)
    build_p.add_argument("entry", nargs="?", default="main.py")

    sub.add_parser("check", help="Validate project structure")

    args = parser.parse_args(argv)
    if args.cmd == "version" or args.cmd is None:
        print(f"echoui {__version__}")
        return 0
    if args.cmd == "new":
        return cmd_new(args.name)
    if args.cmd == "dev":
        return cmd_dev(args.entry, host=args.host, port=args.port, target=args.target)
    if args.cmd == "build":
        return cmd_build(args.entry, target=args.target, out=args.out)
    if args.cmd == "check":
        return cmd_check()
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


def cmd_build(entry: str, *, target: str, out: str | None) -> int:
    app = _load_app(entry)
    out_dir = out or f"dist/{target}"
    path = app.compile(target=target, out_dir=out_dir)
    print(f"Built {target} -> {path}")
    return 0


def cmd_dev(entry: str, *, host: str, port: int, target: str) -> int:
    app = _load_app(entry)
    dev_server(app, host=host, port=port)
    return 0


def cmd_check() -> int:
    ok = True
    for p in ("main.py", "echoui"):
        if not Path(p).exists():
            print(f"Missing: {p}")
            ok = False
    if ok:
        print("check: ok")
    return 0 if ok else 1


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
