# EchoUI Delivery Plan

## DoD
- [x] Version 0.9.0 aligned in pyproject / package / CHANGELOG / docs-src
- [x] Local CI equivalent green: ruff, mypy, pytest
- [x] `python -m build` + `twine check dist/*` pass
- [x] Initial git commit on `main` (no push unless requested)

## Non-goals
- Do not require `twine upload` without credentials
- Do not change completed API semantics

## Work items
1. [x] Bump to 0.9.0; fix docs still marked 待实现
2. [x] Quality gate: install extras → ruff → mypy → pytest
3. [x] Build wheel + twine check
4. [x] First git commit on main
5. [x] Relax pinned deps for modern Python wheels (3.14+)

## Verify
```powershell
cd X:\Project\Public\EchoUI
pip install -e ".[web,dev]"
ruff check .
mypy echoui
pytest -q
python -m build
twine check dist/*
```
