# text / button / box

| 字段 | 内容 |
|------|------|
| 规格域 | roles |
| 模块 | `echoui.layout` |
| 引入版本 | 0.1.0 |
| 矩阵行 | §6 内建角色 |

## 一句话

高频内建 role 工厂，编译为各 target 对应控件。

## 最小示例

```python
from echoui import button, col, text

col(text("Hi"), button("Go", on_click=lambda: None))
```

## 测试

- `tests/unit/test_layout.py`
- `examples/02_counter`
