"""v0.9 ecosystem completion tests."""

from __future__ import annotations

import asyncio

from echoui import App, Screen, col, print_view, text
from echoui.a11y import focus_trap, skip_link
from echoui.cli import cmd_devtools
from echoui.collab import Doc, SyncRelay
from echoui.compiler.bundler import build_target
from echoui.platform import clipboard, detect, notifications, share


def test_collab_doc_and_awareness():
    relay = SyncRelay()
    a = Doc(peer_id="a", relay=relay)
    b = Doc(peer_id="b", relay=relay)
    a.set("title", "Hello")
    relay.broadcast(a.session, "title", "Hello")
    assert b.get("title") == "Hello"
    a.set_cursor(10, 20)
    assert a.awareness.list_peers()


def test_platform_memory_apis():
    async def run():
        await clipboard.write_text("copied")
        assert await clipboard.read_text() == "copied"
        await share.share({"title": "x", "url": "https://example.com"})

    asyncio.run(run())
    notifications.show("Hi", body="there")
    assert notifications.history()
    assert share.history()
    assert detect().capabilities


def test_a11y_helpers():
    node = skip_link("#main")
    assert node.role == "link"
    assert focus_trap(True)["data-focus-trap"] is True


def test_print_view_emits_css(tmp_path):
    class P(Screen):
        def build(self):
            return col(text("screen"), print_view(text("print me")))

    out = tmp_path / "web"
    build_target(App(screens=[P], initial="P"), target="web", out_dir=str(out))
    html = (out / "index.html").read_text(encoding="utf-8")
    assert "e-print-view" in html
    assert "@media print" in html


def test_devtools_command(capsys, tmp_path):
    entry = tmp_path / "main.py"
    entry.write_text(
        "from echoui import App, Screen, Store, col, text\n"
        "class S(Store):\n    n: int = 0\n"
        "s = S()\n"
        "class H(Screen):\n"
        "    def build(self):\n"
        "        return col(text(lambda: str(s.n)))\n"
        "app = App(screens=[H], initial='H')\n",
        encoding="utf-8",
    )
    assert cmd_devtools(str(entry)) == 0
    out = capsys.readouterr().out
    assert "signals" in out
    assert "bindings" in out
