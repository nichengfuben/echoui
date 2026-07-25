"""Device capture and sensors (web runtime bridges)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass
class GeoPosition:
    latitude: float
    longitude: float
    accuracy: float = 0.0


class Geolocation:
    async def get(self) -> GeoPosition:
        return GeoPosition(0.0, 0.0)

    def watch(self, on_move: Callable[[GeoPosition], None]) -> int:
        self._watchers = getattr(self, "_watchers", [])
        self._watchers.append(on_move)
        return len(self._watchers)

    def clear_watch(self, watch_id: int) -> None:
        pass


class Camera:
    async def capture(self) -> bytes:
        return b""

    def stream(self, *, facing: str = "environment") -> Any:
        return {"facing": facing}


class ScreenCapture:
    async def record(self, *, seconds: float = 10.0) -> bytes:
        return b""


class Sensors:
    @property
    def accelerometer(self) -> Dict[str, float]:
        return {"x": 0.0, "y": 0.0, "z": 0.0}

    @property
    def compass(self) -> float:
        return 0.0

    @property
    def ambient_light(self) -> float:
        return 1.0

    @property
    def proximity(self) -> float:
        return 0.0


geolocation = Geolocation()
camera = Camera()
screen = ScreenCapture()
sensors = Sensors()
