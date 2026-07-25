"""Runtime performance monitor."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class PerfMonitor:
    counters: Dict[str, int] = field(default_factory=dict)

    def inc(self, name: str, n: int = 1) -> None:
        self.counters[name] = self.counters.get(name, 0) + n

    def snapshot(self) -> Dict[str, int]:
        return dict(self.counters)
