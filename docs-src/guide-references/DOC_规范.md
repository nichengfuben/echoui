# EchoUI 文档编写规范

> 适用于 `docs-src/`、README、CHANGELOG。Agent 阶段文件在 `.claude/docs/`。

---

## 必须遵守

1. **编码：** UTF-8；禁止乱码占位与 lakesheet 等私有 JSON 嵌入 `.md`。
2. **镜像：** 模块文档放 `docs-src/<P>/`，规则见 [docs-src-guide.md](../docs-src-guide.md)。
3. **图片：** `docs-src/assets/` 或 `docs/assets/`，禁止无文件的路径占位。
4. **诚实：** 状态与追踪矩阵一致；禁止文档超前于代码。
5. **示例：** README 只引用已通过测试的 `examples/`。
6. **源码禁词：** `.py` 中禁止 PLAN、阶段文件名、§ 章节号；见 [code-guide.md](./code-guide.md)。

---

## 分层导读

| 读者 | 入口 |
|------|------|
| 新用户 | `README.md` → `examples/` |
| 模块/API | `docs-src/echoui/` |
| 测试 | `docs-src/tests/` + [tests-guide.md](../tests-guide.md) |
| 踩坑 / 混淆 | `guide-references/troubleshooting.md`、`易混淆对照.md` |
| Agent 续作 | `PROGRESS.md` → `.claude/docs/` |

---

## API 条目

见 [API_图鉴模板.md](./API_图鉴模板.md)。

---

## 维护

- 改 API → 同步 `docs-src/echoui/` 图鉴与矩阵。
- 改测试意图 → 同步 `docs-src/tests/`。
