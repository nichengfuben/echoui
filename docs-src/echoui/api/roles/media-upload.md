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

## 造型切换（跑酷示例）

- `save_player_costume()` / `cycle_player_costume()` — 双槽位，须模块级函数（非 lambda）以通过 `validate_local_compile`。
