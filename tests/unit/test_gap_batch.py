"""Gap-batch coverage: ws/sse surface, camera, chain.then_, canvas, workers, storage, tasks, style."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from echoui.api import SSEClient, WebSocketClient, api, sse, ws
from echoui.camera import Camera
from echoui.canvas import canvas
from echoui.chain import MotionChain
from echoui.sprite import Sprite
from echoui.storage import (
    CookieBackend,
    FileBackend,
    configure_storage,
    local,
    session,
)
from echoui.style import rules_to_css
from echoui.tasks import background, flush, schedule, tick_minute
from echoui.workers import registered_workers, run_in_worker, worker


def test_api_ws_sse_factories_and_url_rewrite():
    prev = api.base_url
    try:
        api.base_url = "https://example.com/api"
        w = ws("/live")
        assert isinstance(w, WebSocketClient)
        assert w.url.startswith("wss://example.com")
        assert w.url.endswith("/live")

        s = sse("/events")
        assert isinstance(s, SSEClient)
        assert "example.com" in s.url
        assert s.url.endswith("/events")

        abs_w = ws("ws://localhost:9/x")
        assert abs_w.url == "ws://localhost:9/x"
        abs_s = sse("http://localhost:9/e")
        assert abs_s.url == "http://localhost:9/e"

        assert callable(api.ws)
        assert callable(api.sse)
        assert isinstance(api.ws("/z"), WebSocketClient)
    finally:
        api.base_url = prev


def test_ws_sse_handlers_chain():
    w = WebSocketClient("ws://example.test/ws")
    seen: list[object] = []
    w.on_message(lambda m: seen.append(m)).on_reconnect(lambda: seen.append("re"))
    assert w._on_message is not None
    assert w._on_reconnect is not None

    s = SSEClient("http://example.test/sse")
    s.on_event("tick", lambda d: seen.append(d)).on_message(lambda e, d: seen.append((e, d)))
    assert "tick" in s._handlers


def test_camera_shake_decays_and_zoom_lerps():
    cam = Camera(x=0, y=0, zoom=1.0)
    cam.shake(10, 1.0)
    ox0, oy0 = cam.shake_offset()
    assert abs(ox0) <= 10 and abs(oy0) <= 10
    cam.tick(0.5, {})
    ox1, oy1 = cam.shake_offset()
    # After half duration, magnitude should be ~half (±5).
    assert abs(ox1) <= 5.01 and abs(oy1) <= 5.01
    cam.tick(0.6, {})
    assert cam.shake_offset() == (0.0, 0.0)

    cam.zoom_to(2.0, duration=1.0)
    cam.tick(0.5, {})
    assert abs(cam.zoom - 1.5) < 0.01
    cam.tick(0.5, {})
    assert abs(cam.zoom - 2.0) < 0.01


def test_camera_follow_deadzone():
    cam = Camera(x=0, y=0, lerp=1.0)
    cam.follow("p", lerp=1.0, deadzone=(20, 20))
    cam.tick(0.016, {"p": (10.0, 5.0)})
    # Inside deadzone — no move.
    assert cam.x == 0 and cam.y == 0
    cam.tick(0.016, {"p": (40.0, 0.0)})
    assert cam.x > 0


def test_motion_chain_then_property():
    class Actor(Sprite):
        x: float = 0
        y: float = 0
        rotation: float = 0
        opacity: float = 1.0
        hidden: bool = False

    actor = Actor()

    async def run():
        chain = MotionChain(actor).rotate(90).then_.rotate(90).then_.glide_to(10, 0, 0.01)
        await chain

    asyncio.run(run())
    assert abs(actor.rotation - 180) < 0.01
    assert abs(actor.x - 10) < 0.5


def test_canvas_fluent_ctx():
    layer = canvas(100, 80)
    ctx = layer.ctx()
    ctx.clear("#101020").fill("#f00").pen("#0f0").width(2).circle(10, 10, 5).text("hi", 1, 2)
    ops = [c["op"] for c in layer.commands]
    assert "clear" in ops
    assert "circle" in ops
    assert "text" in ops
    ir = layer.to_ir()
    assert ir.role == "canvas"
    assert ir.props["width"] == 100


def test_worker_submit_and_pool():
    @worker
    def heavy(x: int) -> int:
        return x * 3

    assert heavy(4) == 12
    fut = heavy.submit(5)
    assert fut.result(timeout=2) == 15
    assert "heavy" in registered_workers()
    assert run_in_worker(lambda: 7).result(timeout=2) == 7


def test_container_queries_css():
    css = rules_to_css(
        "card",
        {
            "padding": "8px",
            "container": {"(min-width: 400px)": {"cols": 2, "gap": "12px"}},
        },
    )
    assert "@container (min-width: 400px)" in css
    assert ".card" in css
    assert "cols:2" in css or "cols: 2" in css.replace(" ", "")


def test_file_backend_and_configure_storage(tmp_path: Path):
    path = tmp_path / "local.json"
    fb = FileBackend(path)
    fb.set("theme", "dark")
    assert fb.get("theme") == "dark"
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert raw["theme"] == "dark"
    fb2 = FileBackend(path)
    assert fb2.get("theme") == "dark"

    configure_storage(local_path=tmp_path / "app_local.json")
    local().set("k", "v")
    assert local().get("k") == "v"
    # session remains memory
    session().set("s", "1")
    assert session().get("s") == "1"


def test_cookie_max_age():
    cb = CookieBackend()
    cb.set_cookie("sid", "abc", max_age=0)
    # max_age 0 means already expired on next get if set_at is past
    # Force expire by rewriting meta
    cb._meta["sid"]["set_at"] = 0
    assert cb.get("sid") is None


def test_tasks_schedule_cron_minute():
    seen: list[int] = []

    def job():
        seen.append(1)

    # Reset queue side effects carefully via module queue
    from echoui import tasks as tasks_mod

    tasks_mod._queue._pending.clear()
    tasks_mod._queue._scheduled.clear()

    schedule(job, cron="*/2 * * * *")
    assert tick_minute() == 0  # tick 1, not yet
    assert tick_minute() == 1  # tick 2
    assert seen == [1]
    background(lambda: seen.append(2))
    assert flush() == 1
    assert seen == [1, 2]


def test_gui_build_writes_lowered(tmp_path: Path):
    from echoui import App, Screen, col, text
    from echoui.targets.gui import build_gui

    class H(Screen):
        def build(self):
            return col(text("hello-gui"))

    out = build_gui(App(screens=[H], initial="H"), out_dir=str(tmp_path / "gui"))
    root = Path(out)
    assert (root / "lowered.json").exists()
    assert (root / "run.py").exists()
    data = json.loads((root / "lowered.json").read_text(encoding="utf-8"))
    assert data  # non-empty lowered nodes
    runner = (root / "run.py").read_text(encoding="utf-8")
    assert "render_qt_tree" in runner


def test_page_style_print_html():
    from echoui.print import PageStyle, print_styles, to_print_html

    page = PageStyle(size="A4", margin="1.5cm")
    css = print_styles(page=page)
    assert "@page" in css
    assert "A4" in css
    html = to_print_html("<p>x</p>", title="Inv", page=page)
    assert "Inv" in html and "@page" in html


def test_virtual_list_to_ir():
    from echoui.compiler.emit_roles import render_role_html
    from echoui.data import VirtualList

    vl = VirtualList(items=list(range(50)), item_height=20, viewport_height=100)
    vl.scroll_to(5)
    node = vl.to_ir()
    assert node.role == "virtual_list"
    assert node.props["virtual"] is True
    assert node.props["start_index"] >= 5
    assert node.props["total"] == 50
    assert len(node.children) > 0
    lowered = {
        "id": getattr(node, "id", "vl"),
        "role": node.role,
        "tag": "div",
        "props": node.props,
        "children": [],
    }
    html = render_role_html(
        lowered,
        attrs=' id="vl"',
        cls="e-virtual_list",
        style_attr="",
        inner="",
        kids="",
    ) or ""
    assert "e-virtual-list" in html
    assert "e-virtual-spacer" in html
    assert 'data-total="50"' in html


def test_named_easing_tween():
    from echoui.animation import EASINGS, ease_out_expo, tween

    assert "ease_out_expo" in EASINGS
    values: list[float] = []
    t = tween(0, 10, 0.2, easing="ease_out_expo", on_update=values.append)
    while not t.tick(0.05):
        pass
    assert values[-1] == 10
    assert ease_out_expo(1.0) == 1.0
