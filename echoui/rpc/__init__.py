"""JSON-RPC 2.0 client."""

from __future__ import annotations

import uuid
from typing import Any, Dict, Optional

from echoui.api import ApiClient


class RpcClient:
    def __init__(self, endpoint: str, *, api: Optional[ApiClient] = None) -> None:
        self.endpoint = endpoint
        self._api = api or ApiClient(base_url=endpoint.rsplit("/rpc", 1)[0])

    async def call(self, method: str, params: Optional[Dict[str, Any]] = None) -> Any:
        req = {"jsonrpc": "2.0", "method": method, "params": params or {}, "id": str(uuid.uuid4())}
        data = await self._api._request("POST", self.endpoint, json=req)
        if isinstance(data, dict) and "error" in data:
            raise RuntimeError(str(data["error"]))
        return data.get("result") if isinstance(data, dict) else data
