# Non-Goals（§33）

EchoUI **不**承担以下职责：

1. **后端业务服务器** — 不提供账号系统、数据库 ORM、部署编排；通过 HTTP/GraphQL/WebSocket 与自有后端集成。
2. **100% 无逃生层的跨平台像素级一致** — 枚举 API 覆盖常见 99%；剩余 1% 通过 §25 逃生层到达原生能力。
3. **替换目标平台全部生态** — 不内置 React/Vue 组件库；可在 web 目标通过 escape 嵌入。
4. **未文档化的静默降级** — 不支持的能力应显式失败或标注 `done-degraded`，禁止静默吞错。
5. **PyPI 发布自动化** — CI 验证 build/twine；实际上传需维护者凭据。

Honest boundaries 见 PLAN.md §0.4 与 `PROGRESS.md` Notes。
