"""CLI static server smoke tests."""

from __future__ import annotations

import socket
import threading
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from echoui import App, Screen, col, text
from echoui.compiler.bundler import build_target


class Hi(Screen):
    def build(self):
        return col(text("Hi"))


app = App(screens=[Hi], initial="Hi")


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def test_preview_serves_built_index(tmp_path):
    out = tmp_path / "dist"
    build_target(app, target="web", out_dir=str(out))
    port = _free_port()

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(out.resolve()), **kwargs)

    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        body = urllib.request.urlopen(f"http://127.0.0.1:{port}/index.html", timeout=5).read()
        assert b"Hi" in body or b"__ECHoui_CFG" in body
        runtime = urllib.request.urlopen(f"http://127.0.0.1:{port}/runtime.js", timeout=5).read()
        assert b"fetch(" not in runtime
    finally:
        httpd.shutdown()
