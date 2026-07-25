# stage / overlay — SSS 与浮层

| 项 | 说明 |
|----|------|
| 规格域 | core / overlay |
| 状态 | done |
| 测试 | `tests/integration/test_build_web.py`, `test_free_gpu.py` |
| 示例 | `examples/03_game_free_mode`, `06_runner`, `09_full` |

## Stage（SSS）

```python
class Game(Screen):
    layout = "free"

    def build(self):
        return stage(
            box(..., x=0, y=0, background="#87ceeb"),
            image(lambda: store.sprite_url, x=80, y=lambda: store.y, width=32, height=32),
            width=640, height=360, layout="free", fill_viewport=True,
        )
```

- free 模式：仅带 `background` 的 `box` 进 GPU canvas；`image`/控件保持 DOM（1.2.2+）
- 帧循环：`@on("frame")` → `tick(dt)` 编译为 `frame_script`

## overlay（modal / drawer / sheet）

IR 节点 + `open_signal`；Web 端 `wireOverlays` 切换 `.e-overlay-open`。

```python
from echoui.overlay import modal

modal("关于", open_signal="App.show_about", children=[text("…")])
```

## compile-local 约束

Handler 须编译为客户端 JS：`Store` 赋值、模块级 game 函数、`router.navigate`；**禁止** `build()` 内 lambda 作 `on_click`。
