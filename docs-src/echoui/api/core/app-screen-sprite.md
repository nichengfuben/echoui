# App / Screen / Sprite

| 字段 | 内容 |
|------|------|
| 规格域 | core |
| 模块 | `echoui.app`, `echoui.screen`, `echoui.sprite` |
| 引入版本 | 0.1.0 |
| 矩阵行 | §1 SSS 范式 |

## 一句话

Screen→Stage→Sprite 唯一范式；App 管理多 Screen 与编译入口。

## 最小示例

```python
from echoui import App, Screen, col, text

class Hello(Screen):
    def build(self):
        return col(text("Hello"))

app = App(screens=[Hello], initial="Hello")
```

## 测试

- `tests/unit/test_counter.py`
- `examples/01_hello_web`
