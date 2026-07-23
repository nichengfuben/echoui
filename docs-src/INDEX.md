# docs-src 索引

EchoUI 规范文档镜像根。镜像规则见 [`docs-src-guide.md`](docs-src-guide.md)；测试见 [`tests-guide.md`](tests-guide.md)。

## 规范（横切）

| 文档 | 说明 |
|------|------|
| [docs-src-guide.md](docs-src-guide.md) | 镜像规则、六要素、查阅/更新 |
| [tests-guide.md](tests-guide.md) | 测试结构与文档同步 |
| [guide-references/code-guide.md](guide-references/code-guide.md) | Python 代码规范与禁词 |
| [guide-references/docs-tests-guide.md](guide-references/docs-tests-guide.md) | docs-src / tests 路由摘要 |
| [guide-references/易混淆对照.md](guide-references/易混淆对照.md) | 易混淆 API 对照 |
| [guide-references/troubleshooting.md](guide-references/troubleshooting.md) | 排错指南 |
| [guide-references/API_图鉴模板.md](guide-references/API_图鉴模板.md) | 对外 API 条目模板 |

## 子树镜像

| 镜像路径 | 源路径 |
|----------|--------|
| [echoui/INDEX.md](echoui/INDEX.md) | `echoui/` 包 |
| [tests/INDEX.md](tests/INDEX.md) | `tests/` |
| [examples/INDEX.md](examples/INDEX.md) | `examples/` |

Agent 执行文档（阶段、矩阵）在 `.claude/docs/`，**不得**在源码中引用。
