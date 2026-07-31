"""Live aiohttp transport tests for WebSocket and SSE clients."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

aiohttp = pytest.importorskip("aiohttp")
from aiohttp import web  # noqa: E402

from echoui.api import SSEClient, WebSocketClient, api, sse, ws  # noqa: E402


async def _ws_echo(request: web.Request) -> web.WebSocketResponse:
    ws_resp = web.WebSocketResponse()
    await ws_resp.prepare(request)
    async for msg in ws_resp:
        if msg.type == aiohttp.WSMsgType.TEXT:
            await ws_resp.send_str(f"echo:{msg.data}")
        elif msg.type == aiohttp.WSMsgType.BINARY:
            await ws_resp.send_bytes(b"bin:" + msg.data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            break
    return ws_resp


async def _sse_stream(request: web.Request) -> web.StreamResponse:
    resp = web.StreamResponse(
        status=200,
        reason="OK",
        headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
    await resp.prepare(request)
    await resp.write(b"event: tick\ndata: one\n\n")
    await resp.write(b"data: two\n\n")
    await resp.write(b"event: done\ndata: end\n\n")
    return resp


async def _run_app(app: web.Application) -> tuple[web.AppRunner, str]:
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    # Port from first socket
    sockets = site._server.sockets  # type: ignore[union-attr]
    port = sockets[0].getsockname()[1]
    return runner, f"127.0.0.1:{port}"


def test_websocket_echo_roundtrip():
    async def run() -> None:
        app = web.Application()
        app.router.add_get("/ws", _ws_echo)
        runner, host = await _run_app(app)
        client: WebSocketClient | None = None
        try:
            client = ws(f"ws://{host}/ws")
            seen: list[Any] = []
            client.on_message(lambda m: seen.append(m))
            await client.connect()
            await client.send("hello")
            msg = await client.receive()
            assert msg == "echo:hello"
            assert seen == ["echo:hello"]
            await client.send(b"xy")
            bin_msg = await client.receive()
            assert bin_msg == b"bin:xy"
        finally:
            if client is not None:
                await client.close()
            await runner.cleanup()
            await api.close()

    asyncio.run(run())


def test_sse_event_stream_parsed():
    async def run() -> None:
        app = web.Application()
        app.router.add_get("/events", _sse_stream)
        runner, host = await _run_app(app)
        client: SSEClient | None = None
        try:
            client = sse(f"http://{host}/events")
            events: list[tuple[str, str]] = []
            ticks: list[str] = []
            client.on_event("tick", lambda d: ticks.append(d))
            client.on_message(lambda e, d: events.append((e, d)))
            await client.connect()
            # Wait until stream handlers fire
            for _ in range(50):
                if len(events) >= 3:
                    break
                await asyncio.sleep(0.05)
            assert ("tick", "one") in events
            assert ("message", "two") in events
            assert ("done", "end") in events
            assert ticks == ["one"]
        finally:
            if client is not None:
                await client.close()
            await runner.cleanup()
            await api.close()

    asyncio.run(run())


def test_api_ws_relative_url_against_live_server():
    async def run() -> None:
        app = web.Application()
        app.router.add_get("/live", _ws_echo)
        runner, host = await _run_app(app)
        prev = api.base_url
        client: WebSocketClient | None = None
        try:
            api.base_url = f"http://{host}"
            client = api.ws("/live")  # type: ignore[attr-defined]
            await client.connect()
            await client.send("z")
            assert await client.receive() == "echo:z"
        finally:
            api.base_url = prev
            if client is not None:
                await client.close()
            await runner.cleanup()
            await api.close()

    asyncio.run(run())
