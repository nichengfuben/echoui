# EchoUI — Universal Python-first UI framework

One **Screen–Stage–Sprite** paradigm compiles to Web, desktop, mobile, TUI, and GUI.

**Version:** 1.2.12 · **License:** MIT · **PyPI:** `pip install echoui` · **GitHub:** [nichengfuben/echoui](https://github.com/nichengfuben/echoui)

## 像 npm 一样用

| npm | EchoUI |
|-----|--------|
| `npm install -g vite` | `pip install echoui[web]` |
| `npm create vite@latest my-app` | `echoui new my-app` |
| `npm run build` | `echoui build --target web` |
| `npm run dev` | `echoui dev --port 8765` |

```bash
pip install echoui[web]
echoui new my-app
cd my-app
pip install -e .          # 安装项目依赖（含 echoui）
echoui build --target web
echoui dev --port 8765
```

PyPI 尚未发布目标版本时，可从 GitHub 安装：

```bash
pip install "echoui[web] @ git+https://github.com/nichengfuben/echoui.git"
```

## Quick Start（已有 main.py）

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

```bash
echoui build --target web
echoui dev --port 8765
```

## CLI

| Command | Description |
|---------|-------------|
| `echoui new [name]` | 脚手架（main.py + pyproject.toml） |
| `echoui dev` | 开发服务器（watch + 静态服务） |
| `echoui build --target web\|static\|tui\|desktop\|gui\|android\|ios` | 编译 |
| `echoui preview` | 预览已 build 的 dist |
| `echoui check` | 校验项目 |
| `echoui version` | 版本 |

## 示例

`examples/` 含 hello、counter、跑酷 `06_runner`、全功能 dashboard `07_full_web` 等。

## License

MIT — see [LICENSE](LICENSE).
