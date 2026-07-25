# row / col / style

| 字段 | 内容 |
|------|------|
| 规格域 | layout |
| 模块 | `echoui.layout`, `echoui.style` |
| 引入版本 | 0.1.0 |
| 矩阵行 | §7 布局 / §8 样式 |

## 最小示例

```python
from echoui import col, row, style, text

col(row(text("A"), text("B")), style={"padding": 8})
```

## 测试

- `tests/unit/test_layout.py`
