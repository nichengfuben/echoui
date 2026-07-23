"""Platform detection and capabilities."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Set


@dataclass
class PlatformInfo:
    os: str
    is_web: bool
    is_desktop: bool
    is_mobile: bool
    capabilities: Set[str]


def detect() -> PlatformInfo:
    os_name = sys.platform
    caps: Set[str] = {"reactive", "compiler"}
    is_web = False
    is_desktop = os_name in ("win32", "darwin", "linux")
    is_mobile = False
    if is_desktop:
        caps.add("filesystem")
    return PlatformInfo(
        os=os_name,
        is_web=is_web,
        is_desktop=is_desktop,
        is_mobile=is_mobile,
        capabilities=caps,
    )


def has_capability(name: str) -> bool:
    return name in detect().capabilities
