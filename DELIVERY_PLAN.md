# EchoUI Delivery Plan

## DoD (v0.9 全量)
- [x] Version 0.9.0 aligned in pyproject / package / CHANGELOG / docs-src
- [x] Local CI equivalent green: ruff, mypy, pytest
- [x] `python -m build` + `twine check dist/*` pass
- [x] `py achecker.py` → 0 violations
- [x] User docs under `docs/api/` (getting-started, targets, non-goals, roles)
- [x] `08_全量追踪矩阵.md` synced with PROGRESS (no blank `not-started` on shipped scope)
- [x] Initial git commit on `main` (no push unless requested)

## Non-goals
- Do not require `twine upload` without credentials
- Do not change completed API semantics without documenting degradation

## Work items
1. [x] Bump to 0.9.0; fix docs still marked 待实现
2. [x] Quality gate: ruff → mypy → pytest
3. [x] Build wheel + twine check
4. [x] achecker EchoUI layout exemptions + docs/api fill
5. [x] AGENTS.md / README / PROGRESS / matrix sync
6. [x] CI workflow includes achecker + build smoke

## Verify
```powershell
cd X:\Project\Public\EchoUI
pip install -e ".[web,dev]"
ruff check .
mypy echoui
pytest -q
py achecker.py
python -m build
twine check dist/*
```
