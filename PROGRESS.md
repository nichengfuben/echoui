# EchoUI Progress

> **审计规则**：仅 `[x]` 表示本机命令验证通过。  
> **终态声明（v1.2.10）**：compile-local Web + 造型 API + 09 协议机器检查 + 08 矩阵无 not-started。

## 当前阶段

**v1.2.10 — Web A 类终态**（2026-07-25）

PyPI **1.2.10** · GitHub **v1.2.10** · 141 pytest

---

## 09 协议 — 机器可检查项

| 项 | 状态 | 证据 |
|----|:----:|------|
| `pip install echoui` | [x] | PyPI 1.2.10 |
| `pytest -q` | [x] | 141 passed |
| `mypy echoui` | [x] | 全绿 |
| `ruff check echoui tests` | [x] | 全绿 |
| `python achecker.py` | [x] | 全绿 |
| `python -m build` + `twine check` | [x] | PASSED |
| 九示例 web+static build | [x] | test_build_all_examples |
| tag → PyPI CI | [x] | publish.yml v1.2.10 |
| TUI IR 渲染 | [x] | compose_ir + test_build_tui |
| Desktop build + `.exe` | [x] | test_build_desktop |
| Android Gradle + APK | [x] | test_build_android |
| iOS web bundle | [x] | test_build_ios + ios-build.yml |
| 82 role Web emit 图鉴 | [x] | role-catalog.md |
| Playwright counter+escape | [x] | test_playwright_web.py |
| pycrdt 协作 | [x] | echoui[collab] + test_collab_pycrdt |
| compile-local Web 栈 | [x] | validate_local + Store 信号修复 |
| 造型 API 四件套 | [x] | costume.py + test_costume + 08_media + sprite-costume.md |

---

## 诚实边界（非阻塞 Web 终态）

| 项 | 说明 |
|----|------|
| MotionChain / 全 Sprite 运动面 | 仍为 partial，非 Web 阻塞项 |
| iOS `.ipa` 签名上架 | 需 macOS + Apple 开发者账号 |
| 应用商店审核 | 超出框架范围 |
| TTS / 录音 / 全 platform API | stub 或 not-started，矩阵已标注 |
| 每 role 独立长文 | 82 role 统一图鉴 + 专项文档 |

---

## 与计划对齐摘要

| 计划主题 | 对齐状态 |
|----------|----------|
| SSS + compile-local Web | done |
| 上传 / 贴图 / 造型 | done（框架 API，非游戏内 ad-hoc） |
| Sprite costume / switch / next | done |
| 多端 export（TUI/Desktop/Android/iOS） | partial，有集成测 |
| 全量 PLAN 字面 100% | **未宣称**；08 矩阵 honest partial |

---

## 审计日志

```
2026-07-25 v1.2.10 造型 API + Store 信号 + 08 矩阵 v4 对齐
2026-07-25 v1.2.9 desktop/android/ios/playwright/pycrdt/role-catalog
2026-07-25 v1.2.8 CI publish + docs
2026-07-25 v1.2.7 Web compile-local
```
