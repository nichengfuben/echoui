# Getting Started

## 安装

```bash
pip install echoui[web,dev]
# 或本地开发
pip install -e ".[web,dev]"
```

## Counter 示例

```python
from echoui import App, Screen, Store, col, text, button

class CounterStore(Store):
    count: int = 0

store = CounterStore()

class Counter(Screen):
    def build(self):
        return col(
            text(lambda: f"Count: {store.count}"),
            button("+1", on_click=lambda: setattr(store, "count", store.count + 1)),
        )

app = App(screens=[Counter], initial="Counter")
```

## CLI

| 命令 | 说明 |
|------|------|
| `echoui new [name]` | 脚手架 |
| `echoui dev --target web --port 7999` | 开发服务器 |
| `echoui build --target web` | 编译输出 |
| `echoui check` | 项目校验 |
| `echoui version` | 打印版本 |

完整示例见 `examples/02_counter/`。
