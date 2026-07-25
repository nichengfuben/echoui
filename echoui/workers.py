"""Web Worker bridge for off-main-thread tasks (PLAN § workers)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict


@dataclass
class WorkerBridge:
    """Compile-time worker registration; emitted into web runtime."""

    name: str
    script: str
    handlers: Dict[str, Callable[..., Any]] = field(default_factory=dict)

    def on_message(self, kind: str, handler: Callable[..., Any]) -> "WorkerBridge":
        self.handlers[kind] = handler
        return self
