"""Optimizer pass; no-op until later pipeline stages."""

from __future__ import annotations

from typing import Any, Dict


def optimize(ir_bundle: Dict[str, Any]) -> Dict[str, Any]:
    return ir_bundle
