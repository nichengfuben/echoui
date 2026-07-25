# EchoUI Progress

## 当前阶段

v0.9.2 — **已对齐 PLAN.md**（`docs/api/plan-map.md`）

## 已闭环

- [x] PLAN §30 模块结构：§0–§35 均有代码落点
- [x] PLAN §6：50+ role 工厂可从 `from echoui import chart, map, …` 导入
- [x] PLAN §28：插件装饰器 + `examples/plugins/status_badge`
- [x] PLAN §31：CLI 全命令面（`preview export analyze test doctor add`）
- [x] PLAN §29：`testing.a11y_audit(...).passes`
- [x] PyPI `echoui==0.9.1`；本地 0.9.2 待发布
- [x] pytest 41 passed / mypy / ruff / achecker 0

## 遗留（PLAN 诚实边界）

- Desktop `.exe` / Android `.apk` 本机验证（A 类工具链）
- iOS CI artifact 首次跑通
- GitHub release tag push（网络/远程待稳定）
