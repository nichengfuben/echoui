## Task Completion Requirements

- Environment/configuration health check and static type checking must pass before considering tasks completed.
- Run code style/lint checks (`ruff check .`) — must pass.
- Run `python achecker.py` — must pass with 0 violations.
- Run `pytest -q`, `mypy echoui`, `python -m build`, `twine check dist/*` for release-ready changes.

## Project Snapshot

EchoUI is a Python-first UI framework using the **Screen → Stage → Sprite** paradigm. It compiles to web, static, TUI, desktop, and GUI targets.

Package: `echoui` · Version line: **0.9.0** · License: MIT

## Core Priorities

1. Reactive correctness (Signal / Computed / Store).
2. Compiler + runtime parity across documented targets.
3. Honest capability matrix — mark `done-degraded` or `interface-only` instead of silent stubs.

## Documentation

- User docs: `docs/api/`
- Spec mirror: `docs-src/`
- Phase matrix: `.claude/docs/08_全量追踪矩阵.md` (sync with `PROGRESS.md`)
