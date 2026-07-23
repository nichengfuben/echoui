# docs-src 与 tests 规范索引

路由摘要；细则以权威文档为准。

## 权威文档

| 主题 | 路径 |
|------|------|
| docs-src 镜像、六要素 | [`../docs-src-guide.md`](../docs-src-guide.md) |
| tests 结构与文档同步 | [`../tests-guide.md`](../tests-guide.md) |
| 代码规范与禁词 | [`code-guide.md`](code-guide.md) |
| 总索引 | [`../INDEX.md`](../INDEX.md) |

## 要点

- **镜像**：`docs-src/<P>/` 对应源路径 `<P>/`。
- **测试**：代码在 `tests/`；说明在 `docs-src/tests/`。
- **流程**：改代码前读 docs-src；行为变更后更新 docs-src。
- **源码**：禁止在 `.py` 中引用 PLAN、阶段文件、§ 章节号（见 `code-guide.md`）。
