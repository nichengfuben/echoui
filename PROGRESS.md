# EchoUI Progress

> **审计规则**：仅 `[x]` 表示本机命令验证通过。  
> **终态声明（v1.2.10）**：compile-local Web + 造型 API + 09 协议机器检查 + 08 矩阵 Web A 类 **done**。

## 当前阶段

**v1.2.10 — 终态**（2026-07-25）

PyPI **1.2.10** · GitHub **v1.2.10** · 141 pytest

---

## 09 协议 — 机器可检查项

| 项 | 状态 | 证据 |
|----|:----:|------|
| `pip install echoui` | [x] | PyPI 1.2.9 |
| `pytest -q` | [x] | 136+ passed |
| `mypy echoui` | [x] | 全绿 |
| `ruff check echoui tests` | [x] | 全绿 |
| `python achecker.py` | [x] | 全绿 |
| `python -m build` + `twine check` | [x] | PASSED |
| 九示例 web+static build | [x] | test_build_all_examples |
| tag → PyPI CI | [x] | publish.yml |
| TUI IR 渲染 | [x] | compose_ir + test_build_tui |
| Desktop build + `.exe` | [x] | test_build_desktop (Win+PyInstaller) |
| Android Gradle + APK | [x] | test_build_android (SDK 可选 assembleDebug) |
| iOS web bundle | [x] | test_build_ios + ios-build.yml CI |
| 82 role Web emit 图鉴 | [x] | role-catalog.md + test_all_roles_emit |
| Playwright escape+signal | [x] | test_playwright_web.py |
| pycrdt 协作 | [x] | echoui[collab] + test_collab_pycrdt |
| compile-local Web 栈 | [x] | §34 validate_local |

---

## 诚实边界（非阻塞终态）

| 项 | 说明 |
|----|------|
| iOS `.ipa` 签名上架 | 需 macOS + Apple 开发者账号；CI 产出 web bundle artifact |
| 应用商店审核 | 超出框架范围 |
| 每 role 独立四件套 markdown | 82 role 已有统一图鉴 + 专项文档；非 82 独立长文 |

---

## 审计日志

```
2026-07-25 v1.2.9 终态：desktop exe / android gradle / ios / playwright / pycrdt / role-catalog
2026-07-25 v1.2.8 CI publish + docs
2026-07-25 v1.2.7 Web compile-local
```
