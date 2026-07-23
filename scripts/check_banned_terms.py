#!/usr/bin/env python3
"""Fail if banned internal-doc terms appear in Python sources."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRS = ("echoui", "tests", "examples", "scripts")
PATTERNS = [
    re.compile(r"\bPLAN\b", re.I),
    re.compile(r"§\s*\d"),
    re.compile(r"\.claude/docs"),
    re.compile(r"08_全量追踪"),
    re.compile(r"PHASE_v"),
]


def main() -> int:
    bad: list[str] = []
    for name in SCAN_DIRS:
        base = ROOT / name
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            if path.name == "check_banned_terms.py":
                continue
            text = path.read_text(encoding="utf-8")
            for pat in PATTERNS:
                if pat.search(text):
                    bad.append(f"{path.relative_to(ROOT)}: matches {pat.pattern}")
                    break
    if bad:
        print("Banned terms in Python sources:\n" + "\n".join(bad))
        return 1
    print("check_banned_terms: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
