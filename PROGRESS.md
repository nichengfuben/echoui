# EchoUI Progress

## 当前阶段

v0.9 生态与发布 — **已闭环**（2026-07-25）

## 已闭环（可验证）

- [x] 核心引擎 v0.1–v0.4：reactive / compiler / web+SSR / 逃生层
- [x] 多端 target v0.5–v0.8：web / static / tui / desktop / gui / android（代码+测试）
- [x] v0.9 生态：collab / data / i18n / a11y / plugin / devtools
- [x] `ruff` / `mypy` / `pytest`（37 passed）/ `achecker` 0 违规
- [x] examples 五件套 + tests visual/a11y + docs-src API 图鉴
- [x] `scripts/benchmark_reactive.py` PASS
- [x] PyPI：`pip install echoui==0.9.1` 成功
- [x] CLI 链：`echoui new demo && build web/tui` 成功
- [x] `.github/workflows/ios-build.yml` 已添加

## 遗留（非阻塞发布，面向贡献者）

- [ ] Desktop `.exe` / Android `.apk` 本机产出验证（需 PySide6 / Android SDK）
- [ ] iOS CI workflow 首次远程跑通并下载 artifact
- [ ] GitHub release tag（待 push 远程仓库）

## 已知降级/占位

| 项 | 类别 | 说明 |
|----|------|------|
| iOS 本地构建 | B | macOS CI 绕行 |
| 应用商店签名 | C | 需开发者账号 |
| Web sqlite / os_api / gpu | interface-only | `docs/api/targets.md` |
| WCAG | done-degraded | `a11y_audit` 规则检查 |

## 环境记录

- Python 3.14.6 · PyPI 0.9.0 + 0.9.1 已发布
