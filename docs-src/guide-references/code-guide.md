# EchoUI 代码指南

## 作用

本文件是 EchoUI 仓库的 Python 与包结构规范。改 `echoui/`、`tests/`、`examples/` 前必读；行为变更后同步 `docs-src/` 镜像。

## 代码总原则

1. 所有 Python 文件保留 `from __future__ import annotations`。
2. **Python ≥3.11**；类型标注完整；公开 API 必要时一行中文 docstring。
3. 注释解释**为何 / 否则会怎样**，禁止套话与 emoji。
4. 禁止静默吞错；不支持的能力抛 `UnsupportedCapability`。
5. 优先使用 `uv`；依赖以 `pyproject.toml` 为准。

## 禁词（源码与测试）

以下字符串**不得**出现在 `echoui/`、`tests/`、`examples/`、`scripts/` 的 `.py` 文件中的注释、docstring、字符串字面量（测试断言外部文档内容时除外）：

| 类别 | 禁止示例 |
|------|----------|
| 内部规格文件名 | `PLAN.md`、`PLAN`、`PHASE`、`00_MASTER`、`08_全量追踪` |
| 章节占位符 | `§4`、`§27` 等规格章节引用 |
| 内部文档路径 | `.claude/docs/`、`docs-src/`（在 .py 内引用） |
| 其他项目标识 | 照搬 Provider-Evo / Kitten 等外部仓库名到业务逻辑中 |

**允许：** 模块 docstring 用一句话描述**职责**（如「应用根类型，管理 Screen 与编译入口」），不写「见某某 md」。

**文档侧** 可使用追踪矩阵、阶段文件、规格章节编号；**代码侧** 用模块名与类型名自描述。

门禁建议：CI 或本地脚本 `rg -i 'PLAN|§[0-9]|\.claude/docs' echoui tests examples scripts`。

## import 规范

1. 标准库 → 第三方 → 本地（`from echoui...`），块间空行。
2. `from ... import ...` 在前，`import ...` 在后；同组内字母序。
3. 包内相对导入仅用于同目录；跨包用 `from echoui.xxx`。

## 包结构

- `echoui/`：框架实现。
- `tests/`：pytest，路径对齐包结构（见 `tests-guide.md`）。
- `examples/`：可运行示例，供 README 与集成测试引用。
- `docs-src/`：文档镜像，不含可执行代码。

## 质量门禁

```bash
ruff check .
mypy echoui
pytest -q
```

目录与子项宽度等结构检查：若启用 `achecker.py`，违规时优先真实拆分，禁止注释填充过关。

## 与 WebUI 相关

Web 编译产物调试见 `CLAUDE.local.md` 中 WebUI 规范（仅 agent 本地文件，不进 `.py`）。
