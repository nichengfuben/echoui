# EchoUI — Universal Python-first UI framework

One **Screen–Stage–Sprite** paradigm compiles to Web, desktop, mobile, TUI, and GUI.

**Version:** 0.9.0 · **License:** MIT · **Docs:** [docs/api/INDEX.md](docs/api/INDEX.md)

## Quick Start

```bash
pip install -e ".[web,dev]"
```

Create `main.py`:

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

Build and run:

```bash
echoui build --target web
echoui dev --target web --port 7999
```

Open http://127.0.0.1:7999 — click **+1** and the count increments.

## CLI

| Command | Description |
|---------|-------------|
| `echoui new [name]` | Scaffold a counter project |
| `echoui dev --target web` | Dev server with hot reload |
| `echoui build --target web\|static\|tui\|desktop\|gui` | Compile for target |
| `echoui check` | Validate project |
| `echoui version` | Print version |

## Quality Gate

```bash
ruff check .
mypy echoui
pytest -q
python achecker.py
python -m build
twine check dist/*
```

## Testing

```bash
pytest -q
```

## License

MIT — see [LICENSE](LICENSE).
