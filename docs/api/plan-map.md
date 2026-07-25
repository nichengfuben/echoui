# PLAN.md 对齐索引

本文件将 [PLAN.md](../.claude/docs/PLAN.md) 各节映射到仓库落点，便于核对「结构无遗漏」。

| PLAN § | 主题 | 代码落点 |
|--------|------|----------|
| 0 | 通用性保证 | `echoui/raw.py`, `echoui/bridge/`, `examples/05_escape_layer` |
| 1 | SSS 范式 | `app.py`, `screen.py`, `stage.py`, `camera.py`, `sprite.py` |
| 2 | 架构 | `echoui/compiler/`, `echoui/runtime/` |
| 3 | 性能模型 | `echoui/reactive.py`, `scripts/benchmark_reactive.py` |
| 4–5 | 原语 / Sprite API | `sprite.py`, `chain.py` |
| 6 | 内建角色 | `layout.py`, `roles.py`, `from echoui import chart, map, …` |
| 7–8 | 布局 / 样式 | `layout.py`, `style.py` |
| 9 | 反应式 | `reactive.py`, `state.py`, `signals.py` |
| 10 | 事件 / 输入 | `events.py`, `input.py` |
| 11 | 表单 | `forms/` |
| 12 | 存储 | `storage/` |
| 13 | 网络 | `api/`, `graphql/`, `rpc/`, `rtc/`, `query/` |
| 14 | 路由 | `router/` |
| 15 | 异步 | `async_.py`, `workers.py`, `wasm.py`, `tasks.py` |
| 16 | 动画 | `animation.py`, `gestures.py` |
| 17 | 游戏 | `physics.py`, `clone.py`, `tiles.py`, `pathfind.py` |
| 18 | 绘图 | `pen.py`, `canvas.py`, `svg.py`, `three/` |
| 19 | 媒体 | `audio/`, `media/` |
| 20 | 平台 API | `platform/`, `desktop/`, `mobile/` |
| 21 | 窗口 | `overlay.py` |
| 22 | 数据展示 | `data/` |
| 23 | i18n/a11y/print | `i18n/`, `a11y/`, `print/` |
| 24 | 协作 | `collab/` |
| 25 | 逃生层 | `raw.py`, `bridge/` |
| 26 | 目标矩阵 | `docs/api/targets.md`, `targets/` |
| 27 | 编译管线 | `compiler/` |
| 28 | 插件 | `plugin.py`, `examples/plugins/` |
| 29 | 测试 | `testing/`, `tests/` |
| 30 | 模块结构 | 本表 + `echoui/` 目录树 |
| 31 | CLI | `cli.py` — `new dev build preview export analyze check test doctor add` |
| 32 | Roadmap | `PROGRESS.md`, `.claude/docs/08_全量追踪矩阵.md` |
| 33 | Non-Goals | `docs/api/non-goals.md` |
| 34 | 不变量 | `AGENTS.md`, achecker |
| 35 | 包元数据 | `pyproject.toml` |

状态说明见 `08_全量追踪矩阵.md`：`done` / `done-degraded` / `interface-only`。
