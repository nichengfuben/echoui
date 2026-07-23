# tests 文档镜像

**源路径：** `tests/`

## 运行

```bash
pytest -q
ruff check .
mypy echoui
```

## 布局（目标）

```text
tests/
  conftest.py
  unit/           # reactive、compiler、layout
  integration/    # build 产物、CLI
```

路径与 `echoui/` 包结构对齐。细则见 [tests-guide.md](../tests-guide.md)。

## 跳过

外部依赖缺失时使用 `pytest.skip()` 并写明原因。
