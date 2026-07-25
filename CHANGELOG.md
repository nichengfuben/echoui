# Changelog

## 0.9.2

- Align public API with PLAN.md §6: export 50+ built-in role factories from `echoui`
- PLAN §28 plugin decorators: `Plugin`, `compiler_pass`, `role`, `target`, `api_binding`
- PLAN §31 CLI: `preview`, `export`, `analyze`, `test`, `doctor`, `add`; build targets `android`/`ios`
- PLAN §29: `echoui.testing.a11y_audit` with `.passes`
- `docs/api/plan-map.md` — PLAN §0–§35 → module index
- PLAN §15：`async_`/`workers`/`wasm`/`tasks` API 落点
- PLAN §17：`clone_pool` 对象池
- `docs/api/plan-alignment.md` — PLAN 各节对齐摘要

## 0.9.1

- Fix TUI build JSON serialization for reactive lambdas
- Add `python -m echoui` entry via `__main__.py`
- Bootstrap modules, examples `01_hello_web` / `03_game_free_mode`, visual/a11y tests
- docs-src API catalog entries; iOS CI workflow; reactive benchmark script

## 0.9.0

- Release-ready packaging: version aligned across pyproject, package, docs, and CHANGELOG
- Quality gate: ruff, mypy, pytest; wheel build + twine check
- Marks v0.1–v0.9 feature set as the first public-ready cut (see PROGRESS.md)

## 0.1.0

- Reactive core: Signal, Computed, Effect, batch, Store
- Screen–Stage–Sprite paradigm with flow and free layout
- Web compiler pipeline: parser → analyzer → optimizer → lower → emit → bundler
- CLI: new, dev, build, check, version
- Testing harness: mount, fire, tick, snapshot
- Router with guards and middleware
- Forms, storage, query, animation, gestures, overlay
- Escape layer (raw.js/html/css) and bridge.web_api
- Static, TUI, desktop, GUI, Android template targets
- Collab CRDT, data tables, i18n, a11y, print, platform, plugins
