# Sprite 造型 API

| 项 | 说明 |
|----|------|
| 规格域 | core / sprite |
| 状态 | done (1.2.10+) |
| 测试 | `tests/unit/test_costume.py` |
| 示例 | `examples/08_media` |

## 声明式造型（Sprite）

```python
from echoui import Sprite
from echoui.costume import costume

class Player(Sprite):
    role = "sprite"
    costumes = [costume("idle", "idle.png"), costume("run", "run.png")]
    current_costume: str = "idle"

    def build(self):
        return self.image(self.costume_src)

player.switch_costume("run")   # 或 switch_costume(1)
player.next_costume()
```

## Store + compile-local（上传 / 命名切换）

```python
from echoui.costume import CostumeFieldsMixin, bind_costumes, costume

class MediaStore(Store, CostumeFieldsMixin):
    sprite_url: str = ""

controls = bind_costumes(
    MediaStore,
    [costume("idle", ""), costume("run", "")],
    url="sprite_url",
)

image(lambda: store.sprite_url, width=128, height=128)
button("Next", on_click=controls.next_costume)
button("Run", on_click=controls.switch["run"])
button("Save", on_click=controls.save_costume)
```

- `make_costume_handlers(Store, url=...)` — 纯上传追加槽位后循环
- handler 通过 `__echoui_source__` 在 build 时编译为客户端 JS
- 跑酷示例仅单张 `player_url` 上传；造型 UI 见 `08_media`
