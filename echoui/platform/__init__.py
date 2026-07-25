"""Platform and device APIs — memory bridge on dev; UnsupportedCapability on unsupported targets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from echoui.exceptions import UnsupportedCapability

_clipboard_text: str = ""
_notification_log: List[Dict[str, str]] = []
_share_log: List[Dict[str, str]] = []


def _require_web(feature: str) -> None:
    info = detect()
    if not info.is_web and info.os not in ("emscripten",):
        raise UnsupportedCapability(f"{feature} is not available on this target")


@dataclass
class PlatformInfo:
    os: str
    is_web: bool
    is_desktop: bool
    is_mobile: bool
    capabilities: set[str]


def detect() -> PlatformInfo:
    import sys

    os_name = sys.platform
    caps = {"reactive", "compiler", "clipboard", "notifications", "share", "vibration", "files"}
    is_web = os_name == "emscripten"
    is_desktop = os_name in ("win32", "darwin", "linux") and not is_web
    is_mobile = False
    if is_desktop:
        caps.update({"filesystem", "window", "tray", "menubar"})
    return PlatformInfo(
        os=os_name,
        is_web=is_web,
        is_desktop=is_desktop,
        is_mobile=is_mobile,
        capabilities=caps,
    )


def has_capability(name: str) -> bool:
    return name in detect().capabilities


class Notifications:
    def request(self) -> bool:
        return True

    def show(self, title: str, *, body: str = "", icon: str = "") -> None:
        _notification_log.append({"title": title, "body": body, "icon": icon})

    @staticmethod
    def history() -> List[Dict[str, str]]:
        return list(_notification_log)


class Clipboard:
    async def write_text(self, text: str) -> None:
        global _clipboard_text
        _clipboard_text = text

    async def read_text(self) -> str:
        return _clipboard_text


class Share:
    async def share(self, data: Dict[str, str]) -> None:
        _share_log.append(dict(data))

    @staticmethod
    def history() -> List[Dict[str, str]]:
        return list(_share_log)


@dataclass
class Battery:
    level: float = 1.0
    charging: bool = True


@dataclass
class Network:
    online: bool = True
    type: str = "wifi"


class Vibration:
    def __init__(self) -> None:
        self.patterns: List[List[int]] = []

    def vibrate(self, pattern: list[int]) -> None:
        self.patterns.append(list(pattern))


notifications = Notifications()
clipboard = Clipboard()
share = Share()
battery = Battery()
network = Network()
vibration = Vibration()


async def dialog_open_file(*, accept: str = "*/*") -> Optional[str]:
    from echoui.storage.files import files

    if detect().is_desktop:
        return await files.pick(accept=accept)  # type: ignore[return-value]
    _require_web("dialog.open_file")
    return None


async def dialog_save_file(name: str, data: bytes) -> None:
    if detect().is_desktop:
        from echoui.storage.files import files

        await files.save(name, data)
        return
    _require_web("dialog.save_file")
