# PLAN.md 对齐状态（用户向摘要）

完整规格见 [`.claude/docs/PLAN.md`](../../.claude/docs/PLAN.md)。模块落点见 [plan-map.md](plan-map.md)。

| § | 主题 | 对齐状态 | 说明 |
|---|------|----------|------|
| 0–1 | 纲领 / SSS | **done** | Screen→Stage→Sprite；flow/free |
| 2–3 | 架构 / 性能 | **done-degraded** | 编译管线 + benchmark；GPU 路径简化 |
| 4–5 | 原语 / Sprite API | **done-degraded** | 核心 API + MotionChain；高级 sensing 部分 stub |
| 6 | 50+ roles | **done-degraded** | 全部工厂可 `import`；高级渲染降级 |
| 7–8 | 布局 / 样式 | **done-degraded** | row/col/grid + theme；responsive 最小 |
| 9 | 反应式 | **done** | Signal/Store/computed/effect/batch |
| 10 | 事件 / 输入 | **done-degraded** | @on + keyboard/mouse/touch/gamepad stub |
| 11–14 | 表单 / 存储 / 网络 / 路由 | **done-degraded** | 模块存在 + 测试 |
| 15 | 异步 | **done-degraded** | `async_`/`workers`/`wasm`/`tasks` API 落点 |
| 16–18 | 动画 / 游戏 / 绘图 | **done-degraded** | animation/gestures/physics/canvas/svg/three |
| 19–20 | 媒体 / 平台 | **interface-only** | 类型骨架 + UnsupportedCapability |
| 21–24 | 窗口 / 数据 / i18n / 协作 | **done-degraded** | overlay/data/i18n/collab 最小实现 |
| 25 | 逃生层 | **done** | raw.js/html/css + bridge + `05_escape_layer` |
| 26 | 目标矩阵 | **done** | [targets.md](targets.md) |
| 27–31 | 编译 / 插件 / 测试 / CLI | **done-degraded** | 全 CLI 命令面；`echoui test`→pytest |
| 32–35 | Roadmap / 发布 | **done** | PyPI + PROGRESS + 追踪矩阵 |

**诚实边界（PLAN §33）**：非可视化编辑器、非客户端 Python 运行时、非后端框架；单平台独占能力仅在对应 OS 可达。
