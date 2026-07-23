# tests 编写规范

## 一、定位与分工

| 侧 | 路径模式 | 内容 |
|----|----------|------|
| 测试代码 | `tests/` | 可执行的 pytest |
| 测试文档 | `docs-src/tests/` | 测试意图、覆盖范围、与源码对应关系 |

测试目录与所测源码**路径尽量镜像**（相对仓库根 `echoui/`）。测试文档须满足 `docs-src-guide.md` 第三节六要素。

EchoUI 布局示例：

```text
tests/
  unit/           # 纯单元：reactive、compiler、layout
  integration/    # 端到端：build 产物、CLI
  conftest.py
docs-src/tests/
  INDEX.md
  unit/
  integration/
```

## 二、镜像范围

与 `docs-src-guide.md` 第二节相同排除规则。

## 三、结构约定

- `conftest.py`：共享 fixture（mount、临时 dist 目录等）。
- 测试路径对齐 `echoui/` 包结构，例如 `tests/unit/test_reactive.py` 对应 `echoui/reactive.py`。
- 新增可测逻辑时，在 `tests/` 下补齐路径，并更新 `docs-src/tests/` 镜像。

## 四、跳过规则

允许跳过：外部 API 不可用、凭证缺失、Playwright/ Qt 未安装。

必须：`pytest.skip()` 写明原因；不得伪造通过；长期限制记入 `PROGRESS.md` 或 `docs-src/PROJECT_DECISIONS.md`。

## 五、质量门禁

从仓库根执行：

```bash
ruff check .
mypy echoui
pytest -q
```

可选：`python achecker.py`（若仓库启用）。

## 六、文档同步

测试增删改或意图变化时，同步更新 `docs-src/tests/` 下对应镜像文档。

## 七、四件套与矩阵

对外 API 标 `done` 时须齐：**实现 + 单测 + examples + docs-src 图鉴条目**。单测路径须写在 `docs-src/guide-references/API_图鉴模板.md` 对应条目中。
