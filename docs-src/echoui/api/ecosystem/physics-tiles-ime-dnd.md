# Physics / TMX / IME / 文件 DnD

| 字段 | 值 |
|------|-----|
| 规格域 | ecosystem / games / input |
| 状态 | **partial** |
| 测试 | `tests/unit/test_physics_tiles_ime_dnd.py` |
| 示例 | 单测为主（无独立 examples） |

## 职责

- **物理**：默认 AABB `World`；可选 `PymunkWorld` / `create_world("pymunk")`（`echoui[physics]`）。
- **图块**：`TileMap` + `load_tmx`（Tiled 正交 + CSV/base64 layer 子集，可选 gzip/zlib；`collision` 层 solid；`<objectgroup>` 点/矩形/tile-gid）。
- **IME**：`keyboard.composition_*` / `apply_composition_event`；Web `core.js` composition* → `__ime_*` 信号。
- **文件 DnD**：`DropFile` / `DropPayload` / `make_drop_event` / `dispatch_drop`；Web `wireDropTargets`。
- **drop IR**：`layout.drop_target(...)` → `analyze_ui` 第五元组 → lower → `client_cfg.drop_targets`。
- **寻路**：`passable_from_tilemap` / `astar_on_tilemap`（绕 solid 层）。

## 诚实边界

| 能力 | 现实 |
|------|------|
| Box2D-class 全套 | **否** — 内置 AABB；可选 pymunk 子集（非 box2d-py） |
| 完整 TMX | **否** — CSV + base64（gzip/zlib）+ object 点/矩形/gid；无 infinite / zstd / 完整 polygon 顶点 |
| 浏览器 WebRTC / 真设备 | **否**（见 media-rtc-flip） |
| OS 级 IME 桥 | Python 侧状态机 + Web composition 事件；非桌面原生 IME 全路径 |
| drop 全目标 | Web IR 贯通；桌面原生 drop 路径仍弱 |

## 用法摘录

```python
from echoui import drop_target, text
from echoui.physics import create_world, World, Body, AABB
from echoui.tiles import load_tmx, tilemap
from echoui.pathfind import astar_on_tilemap
from echoui.input import apply_composition_event, keyboard
from echoui.events import make_drop_event, dispatch_drop, DropPayload, DropFile

w = create_world("aabb")
tm = load_tmx(open("level.tmx", encoding="utf-8").read())
assert tm.layer("collision").solid
spawn = tm.find_object("player")  # object layer 子集
path = astar_on_tilemap(tm, (0, 1), (3, 1))
apply_composition_event("compositionupdate", "ni")
ev = make_drop_event(files=[{"name": "a.png", "size": 1}])
zone = drop_target(text("drop"), signal="App.meta", file_signal="App.file")
```
