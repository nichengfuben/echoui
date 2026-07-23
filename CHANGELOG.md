# Changelog

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
