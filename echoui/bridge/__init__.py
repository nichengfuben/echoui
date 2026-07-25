"""Native and web escape bridges."""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional


class WebApi:
    """Browser API bridge for escape layer."""

    def __init__(self) -> None:
        self._listeners: Dict[str, list[Callable[..., None]]] = {}

    def add_event_listener(self, event: str, handler: Callable[..., None]) -> None:
        self._listeners.setdefault(event, []).append(handler)

    def dispatch(self, event: str, **payload: Any) -> None:
        for h in self._listeners.get(event, []):
            h(**payload)

    def local_storage_get(self, key: str) -> Optional[str]:
        from echoui.storage import local

        return local().get(key)

    def local_storage_set(self, key: str, value: str) -> None:
        from echoui.storage import local

        local().set(key, value)


def web_api() -> WebApi:
    return WebApi()


def os_api() -> Any:
    from echoui.exceptions import UnsupportedCapability

    raise UnsupportedCapability("os_api is not available on this target")


class WebGpuApi:
    """WebGPU bridge — runtime in ``runtime/web/webgpu.js``."""

    def backend(self) -> str:
        return "webgpu"

    def supports(self) -> bool:
        return True


def gpu_api() -> WebGpuApi:
    return WebGpuApi()
