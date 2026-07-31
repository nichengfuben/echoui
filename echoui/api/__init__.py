"""HTTP and WebSocket client."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple

try:
    import aiohttp
except ImportError:
    aiohttp = None  # type: ignore[assignment]

InterceptorFn = Callable[[Dict[str, Any]], Dict[str, Any]]
ProgressFn = Callable[[int, int], None]


def chunk_ranges(
    total: int,
    chunk_size: int,
    *,
    resume_from: int = 0,
) -> List[Tuple[int, int]]:
    """Return inclusive ``(start, end)`` byte ranges for a sequential chunk upload.

    ``end`` is inclusive (Content-Range style). Empty payload yields one ``(0, -1)``
    sentinel so callers still fire a single zero-length finalization step.

    ``resume_from`` skips already-uploaded bytes (offset subset, not full tus):
    ranges whose ``end < resume_from`` are dropped; a straddling first range is
    trimmed so ``start == resume_from``. When ``resume_from >= total`` and
    ``total > 0``, returns an empty list (nothing left to send).
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if total < 0:
        raise ValueError("total must be non-negative")
    if resume_from < 0:
        raise ValueError("resume_from must be non-negative")
    if total == 0:
        if resume_from > 0:
            raise ValueError("resume_from exceeds total")
        return [(0, -1)]
    if resume_from > total:
        raise ValueError("resume_from exceeds total")
    if resume_from == total:
        return []
    ranges: List[Tuple[int, int]] = []
    start = 0
    while start < total:
        end = min(start + chunk_size, total) - 1
        ranges.append((start, end))
        start = end + 1
    if resume_from == 0:
        return ranges
    out: List[Tuple[int, int]] = []
    for start, end in ranges:
        if end < resume_from:
            continue
        if start < resume_from:
            start = resume_from
        out.append((start, end))
    return out


def iter_byte_chunks(
    data: bytes,
    chunk_size: int,
    *,
    resume_from: int = 0,
) -> Iterator[Tuple[int, int, bytes]]:
    """Yield ``(start, end_inclusive, slice)`` for each remaining chunk of ``data``."""
    total = len(data)
    for start, end in chunk_ranges(total, chunk_size, resume_from=resume_from):
        if end < start:
            yield start, end, b""
        else:
            yield start, end, data[start : end + 1]


@dataclass
class ApiClient:
    base_url: str = ""
    timeout: float = 30.0
    retries: int = 1
    interceptors: List[InterceptorFn] = field(default_factory=list)
    _session: Any = field(default=None, repr=False)

    async def _get_session(self) -> Any:
        if aiohttp is None:
            raise ImportError("aiohttp required; pip install echoui[web]")
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    async def get(self, path: str, **kwargs: Any) -> Any:
        return await self._request("GET", path, **kwargs)

    async def post(self, path: str, **data: Any) -> Any:
        return await self._request("POST", path, json=data)

    async def upload(
        self,
        path: str,
        field: str,
        data: bytes,
        filename: str = "file",
        *,
        on_progress: Optional[ProgressFn] = None,
    ) -> Any:
        """Single-shot multipart upload. Optional ``on_progress(sent, total)`` once done."""
        if aiohttp is None:
            raise ImportError("aiohttp required")
        session = await self._get_session()
        form = aiohttp.FormData()
        form.add_field(field, data, filename=filename)
        url = self.base_url + path
        async with session.post(url, data=form) as resp:
            result = await resp.json()
        if on_progress is not None:
            on_progress(len(data), len(data))
        return result

    async def upload_chunked(
        self,
        path: str,
        data: bytes,
        *,
        field: str = "file",
        filename: str = "file",
        chunk_size: int = 256 * 1024,
        resume_from: int = 0,
        on_progress: Optional[ProgressFn] = None,
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Sequential chunked upload with ``Content-Range`` on each part.

        Each chunk is a multipart POST of ``field`` with headers::

            Content-Range: bytes start-end/total
            Upload-Offset: <next byte after this chunk>
            X-Chunk-Index / X-Chunk-Count

        ``resume_from`` skips already-accepted bytes (offset subset — not full
        tus CREATE/HEAD/PATCH). When nothing remains, reports progress once and
        returns ``None``.

        Returns the last non-empty JSON/text response (or ``None`` if all empty).
        Pure range planning is available via :func:`chunk_ranges` without network.
        """
        if aiohttp is None:
            raise ImportError("aiohttp required; pip install echoui[web]")
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        session = await self._get_session()
        url = self.base_url + path
        total = len(data)
        ranges = chunk_ranges(total, chunk_size, resume_from=resume_from)
        last: Any = None
        sent = min(resume_from, total)
        if not ranges:
            if on_progress is not None:
                on_progress(sent, total)
            return None
        for index, (start, end, piece) in enumerate(
            iter_byte_chunks(data, chunk_size, resume_from=resume_from)
        ):
            form = aiohttp.FormData()
            form.add_field(field, piece, filename=filename)
            if end < start:
                content_range = f"bytes */{total}"
                next_offset = total
            else:
                content_range = f"bytes {start}-{end}/{total}"
                next_offset = end + 1
            headers = {
                "Content-Range": content_range,
                "Upload-Offset": str(next_offset),
                "X-Chunk-Index": str(index),
                "X-Chunk-Count": str(len(ranges)),
            }
            if extra_headers:
                headers.update(extra_headers)
            async with session.post(url, data=form, headers=headers) as resp:
                resp.raise_for_status()
                ct = resp.headers.get("Content-Type", "")
                if "json" in ct:
                    last = await resp.json()
                else:
                    body = await resp.text()
                    last = body if body else last
            if end >= start:
                sent = end + 1
            if on_progress is not None:
                on_progress(sent, total)
        return last

    async def download(self, path: str, *, on_progress: Optional[ProgressFn] = None) -> bytes:
        session = await self._get_session()
        url = self.base_url + path
        async with session.get(url) as resp:
            total_hdr = resp.headers.get("Content-Length")
            total = int(total_hdr) if total_hdr and total_hdr.isdigit() else 0
            if on_progress is None:
                return await resp.read()
            chunks: List[bytes] = []
            sent = 0
            async for block in resp.content.iter_chunked(64 * 1024):
                chunks.append(block)
                sent += len(block)
                on_progress(sent, total or sent)
            return b"".join(chunks)

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        ctx: Dict[str, Any] = {"method": method, "path": path, **kwargs}
        for ic in self.interceptors:
            ctx = ic(ctx)
        session = await self._get_session()
        url = self.base_url + path
        last_err: Optional[Exception] = None
        for attempt in range(self.retries + 1):
            try:
                async with session.request(method, url, **kwargs) as resp:
                    resp.raise_for_status()
                    ct = resp.headers.get("Content-Type", "")
                    if "json" in ct:
                        return await resp.json()
                    return await resp.text()
            except Exception as e:
                last_err = e
                if attempt < self.retries:
                    await asyncio.sleep(0.1 * (attempt + 1))
        raise last_err  # type: ignore[misc]


api = ApiClient()


class WebSocketClient:
    """Minimal WebSocket client (aiohttp when available)."""

    def __init__(self, url: str, *, api: Optional[ApiClient] = None) -> None:
        self.url = url
        self._api = api
        self._ws: Any = None
        self._on_message: Optional[Callable[[Any], None]] = None
        self._on_reconnect: Optional[Callable[[], None]] = None
        self._closed = False

    def on_message(self, handler: Callable[[Any], None]) -> "WebSocketClient":
        self._on_message = handler
        return self

    def on_reconnect(self, handler: Callable[[], None]) -> "WebSocketClient":
        self._on_reconnect = handler
        return self

    async def connect(self) -> None:
        if aiohttp is None:
            raise ImportError("aiohttp required; pip install echoui[web]")
        session = await (self._api._get_session() if self._api else ApiClient()._get_session())
        self._ws = await session.ws_connect(self.url)
        self._closed = False

    async def send(self, data: Any) -> None:
        if self._ws is None:
            await self.connect()
        assert self._ws is not None
        if isinstance(data, (bytes, bytearray)):
            await self._ws.send_bytes(bytes(data))
        elif isinstance(data, str):
            await self._ws.send_str(data)
        else:
            import json

            await self._ws.send_str(json.dumps(data))

    async def receive(self) -> Any:
        if self._ws is None:
            await self.connect()
        assert self._ws is not None
        msg = await self._ws.receive()
        if msg.type == aiohttp.WSMsgType.TEXT:
            data = msg.data
            if self._on_message:
                self._on_message(data)
            return data
        if msg.type == aiohttp.WSMsgType.BINARY:
            if self._on_message:
                self._on_message(msg.data)
            return msg.data
        if msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
            self._closed = True
            if self._on_reconnect:
                self._on_reconnect()
        return None

    async def close(self) -> None:
        self._closed = True
        if self._ws is not None:
            await self._ws.close()
            self._ws = None


class SSEClient:
    """Server-Sent Events client (aiohttp stream)."""

    def __init__(self, url: str, *, api: Optional[ApiClient] = None) -> None:
        self.url = url
        self._api = api
        self._handlers: Dict[str, List[Callable[[str], None]]] = {}
        self._on_any: Optional[Callable[[str, str], None]] = None
        self._task: Optional[asyncio.Task[Any]] = None
        self._stop = False

    def on_event(self, event: str, handler: Callable[[str], None]) -> "SSEClient":
        self._handlers.setdefault(event, []).append(handler)
        return self

    def on_message(self, handler: Callable[[str, str], None]) -> "SSEClient":
        self._on_any = handler
        return self

    async def connect(self) -> None:
        if aiohttp is None:
            raise ImportError("aiohttp required; pip install echoui[web]")
        session = await (self._api._get_session() if self._api else ApiClient()._get_session())
        self._stop = False

        async def _run() -> None:
            async with session.get(self.url, headers={"Accept": "text/event-stream"}) as resp:
                event = "message"
                data_lines: List[str] = []
                async for raw in resp.content:
                    if self._stop:
                        break
                    line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
                    if line.startswith("event:"):
                        event = line[6:].strip() or "message"
                    elif line.startswith("data:"):
                        data_lines.append(line[5:].lstrip())
                    elif line == "":
                        if data_lines:
                            payload = "\n".join(data_lines)
                            for h in self._handlers.get(event, []):
                                h(payload)
                            if self._on_any:
                                self._on_any(event, payload)
                        event = "message"
                        data_lines = []

        self._task = asyncio.create_task(_run())

    async def close(self) -> None:
        self._stop = True
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None


def ws(path: str, *, base_url: str | None = None) -> WebSocketClient:
    """Create a WebSocket client. ``path`` may be absolute ``ws://`` or relative."""
    if path.startswith("ws://") or path.startswith("wss://"):
        url = path
    else:
        root = (base_url if base_url is not None else api.base_url) or ""
        if root.startswith("https://"):
            root = "wss://" + root[len("https://") :]
        elif root.startswith("http://"):
            root = "ws://" + root[len("http://") :]
        url = root.rstrip("/") + "/" + path.lstrip("/")
    return WebSocketClient(url, api=api)


def sse(path: str, *, base_url: str | None = None) -> SSEClient:
    """Create an SSE client. ``path`` may be absolute ``http(s)://`` or relative."""
    if path.startswith("http://") or path.startswith("https://"):
        url = path
    else:
        root = (base_url if base_url is not None else api.base_url) or ""
        url = root.rstrip("/") + "/" + path.lstrip("/")
    return SSEClient(url, api=api)


# Attach protocol helpers on the default client for ``api.ws`` / ``api.sse`` style.
api.ws = ws  # type: ignore[attr-defined]
api.sse = sse  # type: ignore[attr-defined]
