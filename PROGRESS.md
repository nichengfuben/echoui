# EchoUI Progress

## 当前阶段

v0.9.2 — **PLAN.md 对齐 + 发布闭环**（2026-07-25）

## 已闭环（09 协议机器检查）

- [x] `pip install echoui==0.9.2` 成功
- [x] `ruff` / `mypy` / `pytest` 47 passed / `achecker` 0
- [x] CLI 链：`echoui new` → `build web/tui`
- [x] GitHub：`https://github.com/nichengfuben/echoui` + tag `v0.9.2` + release
- [x] PyPI：https://pypi.org/project/echoui/0.9.2/

## PLAN.md 对齐（见 `docs/api/plan-alignment.md`）

- [x] §6  50+ role 工厂从 `echoui` 导出
- [x] §15 `async_`/`workers`/`wasm`/`tasks` API
- [x] §17 `clone_pool`
- [x] §28 插件装饰器 + 示例
- [x] §29 `testing.a11y_audit`
- [x] §31 CLI 全命令面
- [x] §30 模块落点索引 `docs/api/plan-map.md`

## 遗留（诚实边界，非阻塞发布）

- [ ] Desktop `.exe` / Android `.apk` 本机产出验证
- [ ] iOS CI workflow 首次跑通并下载 artifact
- [ ] 高级 role（chart/map/gantt）target 级真实渲染（当前 done-degraded）
