# file_input / image / audio — 媒体与上传

| 项 | 说明 |
|----|------|
| 规格域 | roles / media / compile-local |
| 状态 | done (1.2.5+) |
| 测试 | `tests/unit/test_media_features.py` |
| 示例 | `examples/06_runner`, `examples/08_media` |

## file_input

```python
file_input("avatar", accept="image/*", signal="App.avatar_url", label="头像")
```

- Web emit `type=file`；`ui.wireFiles` 用 FileReader → data URL 写入 Signal
- **注意**：须使用 `layout.file_input`（1.2.5 前工厂覆盖会导致 `file_inputs` 为空）

## image 响应式 src

```python
image(lambda: store.avatar_url, width=64, height=64)
```

编译为 `attr` 绑定 `{Store.field}` → `img.src`。

## audio.play（compile-local）

```python
from echoui.audio import audio

@on("keydown", key="Space")
def jump(self, _):
    jump()
    audio.play("assets/jump.mp3")
```

构建时写入 client cfg；`audio.js` 在浏览器播放，无 Python 往返。

## 造型切换（`echoui.costume`）

框架内置 API，**不要**在游戏逻辑里手写槽位。

### Sprite 声明式（运行时 / 编译）

```python
from echoui import Sprite
from echoui.costume import costume

class Player(Sprite):
    costumes = [costume("idle", "idle.png"), costume("run", "run.png")]
    current_costume: str = "idle"
    def build(self):
        return self.image(self.costume_src)

player.switch_costume("run")   # 或 switch_costume(1)
player.next_costume()
```

### Store + compile-local（上传 / 命名切换）

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
button("Save", on_click=controls.save_costume)  # 上传后追加槽位
```

示例：`examples/08_media`。跑酷仅保留单张 `player_url` 上传，不含造型 UI。
