"""Chunk range planning and live chunked upload (aiohttp)."""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List

import pytest

from echoui.api import ApiClient, chunk_ranges, iter_byte_chunks


def test_chunk_ranges_basic():
    assert chunk_ranges(10, 4) == [(0, 3), (4, 7), (8, 9)]
    assert chunk_ranges(5, 5) == [(0, 4)]
    assert chunk_ranges(5, 10) == [(0, 4)]
    assert chunk_ranges(0, 4) == [(0, -1)]


def test_chunk_ranges_resume_from():
    # Full plan then skip first 5 bytes of 16 with size 5.
    assert chunk_ranges(16, 5, resume_from=0) == [(0, 4), (5, 9), (10, 14), (15, 15)]
    assert chunk_ranges(16, 5, resume_from=5) == [(5, 9), (10, 14), (15, 15)]
    # Mid-chunk offset trims first range start.
    assert chunk_ranges(16, 5, resume_from=7) == [(7, 9), (10, 14), (15, 15)]
    assert chunk_ranges(16, 5, resume_from=16) == []
    with pytest.raises(ValueError, match="resume_from"):
        chunk_ranges(16, 5, resume_from=17)
    with pytest.raises(ValueError, match="resume_from"):
        chunk_ranges(16, 5, resume_from=-1)


def test_chunk_ranges_rejects_bad_size():
    with pytest.raises(ValueError, match="chunk_size"):
        chunk_ranges(10, 0)
    with pytest.raises(ValueError, match="total"):
        chunk_ranges(-1, 4)


def test_iter_byte_chunks_reassembles():
    data = b"abcdefghij"
    parts = list(iter_byte_chunks(data, 3))
    assert [p[2] for p in parts] == [b"abc", b"def", b"ghi", b"j"]
    assert parts[0][:2] == (0, 2)
    assert parts[-1][:2] == (9, 9)
    assert b"".join(p[2] for p in parts) == data


def test_iter_byte_chunks_resume_from():
    data = b"abcdefghij"
    parts = list(iter_byte_chunks(data, 3, resume_from=4))
    assert parts[0][:2] == (4, 5)
    assert parts[0][2] == b"ef"
    assert b"".join(p[2] for p in parts) == data[4:]


def test_upload_chunked_live_progress():
    pytest.importorskip("aiohttp")
    from aiohttp import web

    async def run() -> None:
        received: List[Dict[str, Any]] = []

        async def handler(request: web.Request) -> web.Response:
            body = await request.read()
            received.append(
                {
                    "range": request.headers.get("Content-Range"),
                    "offset": request.headers.get("Upload-Offset"),
                    "index": request.headers.get("X-Chunk-Index"),
                    "count": request.headers.get("X-Chunk-Count"),
                    "len": len(body),
                }
            )
            return web.json_response({"ok": True, "n": len(received)})

        app = web.Application()
        app.router.add_post("/up", handler)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "127.0.0.1", 0)
        await site.start()
        sockets = site._server.sockets  # type: ignore[union-attr]
        port = sockets[0].getsockname()[1]
        client = ApiClient(base_url=f"http://127.0.0.1:{port}")
        progress: List[tuple[int, int]] = []
        try:
            data = b"0123456789ABCDEF"  # 16 bytes
            result = await client.upload_chunked(
                "/up",
                data,
                chunk_size=5,
                on_progress=lambda s, t: progress.append((s, t)),
            )
            assert result == {"ok": True, "n": 4}
            assert len(received) == 4
            assert received[0]["range"] == "bytes 0-4/16"
            assert received[0]["offset"] == "5"
            assert received[1]["range"] == "bytes 5-9/16"
            assert received[2]["range"] == "bytes 10-14/16"
            assert received[3]["range"] == "bytes 15-15/16"
            assert received[3]["offset"] == "16"
            assert received[0]["count"] == "4"
            assert [r["index"] for r in received] == ["0", "1", "2", "3"]
            assert progress == [(5, 16), (10, 16), (15, 16), (16, 16)]
        finally:
            await client.close()
            await runner.cleanup()

    asyncio.run(run())


def test_upload_chunked_live_resume_from():
    pytest.importorskip("aiohttp")
    from aiohttp import web

    async def run() -> None:
        received: List[Dict[str, Any]] = []
        assembled = bytearray(16)

        async def handler(request: web.Request) -> web.Response:
            cr = request.headers.get("Content-Range", "")
            # bytes start-end/total
            span = cr.split(" ", 1)[-1]
            start_s, rest = span.split("-", 1)
            end_s, total_s = rest.split("/", 1)
            start, end = int(start_s), int(end_s)
            body = await request.read()
            # multipart framing — extract last binary-ish payload roughly via raw body
            # For test stability, re-upload pure bytes via Content-Range only and
            # track headers; reassemble using known data slices on client side.
            received.append(
                {
                    "range": cr,
                    "offset": request.headers.get("Upload-Offset"),
                    "index": request.headers.get("X-Chunk-Index"),
                    "count": request.headers.get("X-Chunk-Count"),
                    "start": start,
                    "end": end,
                    "total": int(total_s),
                    "body_len": len(body),
                }
            )
            # Fill placeholder so we can assert coverage of remaining bytes.
            for i in range(start, end + 1):
                assembled[i] = 1
            return web.json_response({"ok": True, "n": len(received), "offset": end + 1})

        app = web.Application()
        app.router.add_post("/up", handler)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "127.0.0.1", 0)
        await site.start()
        sockets = site._server.sockets  # type: ignore[union-attr]
        port = sockets[0].getsockname()[1]
        client = ApiClient(base_url=f"http://127.0.0.1:{port}")
        progress: List[tuple[int, int]] = []
        try:
            data = b"0123456789ABCDEF"
            # Pretend first 7 bytes already accepted.
            result = await client.upload_chunked(
                "/up",
                data,
                chunk_size=5,
                resume_from=7,
                on_progress=lambda s, t: progress.append((s, t)),
            )
            assert result == {"ok": True, "n": 3, "offset": 16}
            assert len(received) == 3
            assert received[0]["range"] == "bytes 7-9/16"
            assert received[0]["offset"] == "10"
            assert received[0]["index"] == "0"
            assert received[0]["count"] == "3"
            assert received[1]["range"] == "bytes 10-14/16"
            assert received[2]["range"] == "bytes 15-15/16"
            assert progress == [(10, 16), (15, 16), (16, 16)]
            # Bytes 0..6 untouched; 7..15 marked.
            assert list(assembled[:7]) == [0] * 7
            assert all(assembled[7:])

            # Already complete: no POSTs, single progress report.
            received.clear()
            progress.clear()
            done = await client.upload_chunked(
                "/up",
                data,
                chunk_size=5,
                resume_from=16,
                on_progress=lambda s, t: progress.append((s, t)),
            )
            assert done is None
            assert received == []
            assert progress == [(16, 16)]
        finally:
            await client.close()
            await runner.cleanup()

    asyncio.run(run())
