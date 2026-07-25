# EchoUI Progress

## Final Status: Complete (v0.9.0)

All v0.1–v0.9 deliverables implemented with passing tests, build, and achecker.

| Area | Status |
|------|--------|
| Reactive core (Signal, Computed, Store) | Done |
| Screen / Stage / Sprite / Camera | Done |
| Layout (row, col, grid, stack, free) | Done |
| Compiler pipeline (web + SSR) | Done |
| CLI (new, dev, build, check) | Done |
| Testing (mount, fire, tick, snapshot) | Done |
| Router + guards + middleware | Done |
| API client (aiohttp) | Done |
| Forms + validators | Done |
| Storage (local, session, sqlite) | Done |
| Query layer | Done |
| Animation + gestures + overlay | Done |
| Escape layer + bridge | Done |
| Physics, canvas, SVG, tiles, pathfind | Done |
| Targets: web, static, tui, desktop, gui, android | Done |
| Collab, data, i18n, a11y, print, platform, plugin | Done |
| Examples + tests + CI | Done |
| User docs `docs/api/` | Done |
| PLAN §0–§35 tracking matrix | Synced (see `.claude/docs/08_全量追踪矩阵.md`) |
| achecker 0 violations | Done |

## Notes

- v0.1 compiler uses runtime introspection (static analysis planned for later).
- Web sqlite and os_api/gpu backends are **interface-only** (B class); documented in `docs/api/targets.md`.
- Desktop/GUI require optional PySide6 extras.
- PyPI upload is optional; wheel build + `twine check` verified locally.

## v0.9 Release Checklist

- [x] Version 0.9.0 in pyproject / `__init__` / CHANGELOG
- [x] ruff / mypy / pytest green
- [x] `python -m build` + `twine check`
- [x] `py achecker.py` → 0
- [x] `docs/api/` populated
- [x] Git commit on `main`
- [ ] PyPI publish (needs maintainer token)
- [ ] GitHub release tag (needs remote + token)
