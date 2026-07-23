"""HTTP and WebSocket client."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

try:
    import aiohttp
except ImportError:
    aiohttp = None  # type: ignore[assignment]

InterceptorFn = Callable[[Dict[str, Any]], Dict[str, Any]]


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

    async def upload(self, path: str, field: str, data: bytes, filename: str = "file") -> Any:
        if aiohttp is None:
            raise ImportError("aiohttp required")
        session = await self._get_session()
        form = aiohttp.FormData()
        form.add_field(field, data, filename=filename)
        url = self.base_url + path
        async with session.post(url, data=form) as resp:
            return await resp.json()

    async def download(self, path: str) -> bytes:
        session = await self._get_session()
        url = self.base_url + path
        async with session.get(url) as resp:
            return await resp.read()

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
