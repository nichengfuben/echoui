# media / rtc / flip

| 项 | 说明 |
|----|------|
| 规格域 | media · rtc · animation(FLIP) · api.ws/sse 传输 |
| 状态 | partial（诚实 sim + 进程内 RTC + FLIP API + aiohttp 真传输） |
| 测试 | `test_media_rtc_flip.py` · `test_ws_sse_transport.py` |
| 示例 | `examples/08_media`（造型/媒体子集）；RTC/FLIP 以单测为准 |

## media — 诚实能力模型

默认宿主 **不**假成功：`geolocation` / `camera` / `screen` / `sensors` 无桥时抛 `UnsupportedCapability`。  
测试或本地演示：`enable_media_sim()`（或 `enable_capability_sim(...)`）。

```python
import asyncio
from echoui.exceptions import UnsupportedCapability
from echoui.media import camera, clear_media_sim, enable_media_sim, geolocation, screen, sensors

async def demo():
    try:
        await geolocation.get()
    except UnsupportedCapability:
        pass
    enable_media_sim()
    pos = await geolocation.get()
    geolocation.set_sim_position(31.2, 121.5)
    frame = await camera.capture()
    blob = await screen.record(seconds=1.0)
    sensors.set_sim(accel={"x": 1.0, "y": 0.0, "z": -1.0}, compass=90.0)
    assert sensors.compass == 90.0
    clear_media_sim()

asyncio.run(demo())
```

**诚实边界**：sim 为进程内内存桩，不是浏览器 `getUserMedia` / 系统 GPS。

## rtc — 进程内 DataChannel

`RTCPeer` / `DataChannel` 提供 **进程内** 消息投递与 offer/answer 配对，供 collab/测试使用。  
**不是** 浏览器 WebRTC / ICE / DTLS。

```python
from echoui.rtc import RTCPeer

a, b = RTCPeer(), RTCPeer()
ca = a.create_data_channel("game")
cb = b.create_data_channel("game")
got: list[str] = []
cb.on_message = got.append
a.connect(b)
ca.send("ping")
assert got == ["ping"]
```

也可 `DataChannel.pair(other)` 双向绑定，或 `create_offer` / `create_answer` / `apply_answer` 自动配对唯一对端。

## animation.flip — FLIP 列表重排

```python
from echoui.animation import Rect, capture_rects, flip, invert_rects

first = capture_rects({"a": (0.0, 0.0), "b": (0.0, 40.0)})
last = capture_rects({"a": (0.0, 40.0), "b": (0.0, 0.0)})
assert invert_rects(first, last)[0].dy == -40.0  # key a
anim = flip(first, last, duration=0.2, easing="linear")
anim.tick(0.1)  # 半程 invert residual
anim.tick(0.1)  # 结束于 0,0
```

Web emit 侧列表 `animate="auto"` 仍为后续接线；本 API 供 runtime / 测试驱动。

## api.ws / api.sse — 真传输（aiohttp）

可选依赖 `aiohttp` 时，`ws()` / `sse()` / `api.ws` 对真实服务器做 connect/send/receive 与 SSE 解析。  
见 `tests/unit/test_ws_sse_transport.py`（本地 echo / event-stream 服务）。
