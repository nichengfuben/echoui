# platform / a11y / print / devtools (v0.9)

| 项 | 说明 |
|----|------|
| 规格域 | platform / a11y / print / CLI devtools |
| 状态 | partial（宿主内存桥 + 硬件 API 显式 UnsupportedCapability） |
| 测试 | `test_ecosystem_v09.py` · `test_platform_honesty.py` |
| 示例 | `examples/07_full_web`（i18n/a11y 子集） |

## platform — 诚实能力模型

**宿主可用（进程内内存/日志桥，非系统剪贴板/系统通知）：**

- `clipboard` / `notifications` / `share` / `vibration` / `battery` / `network`
- 桌面 `dialog_open_file` / `dialog_save_file` 委托 `files`（tkinter 选文件）

**硬件/系统 API（无 native/web 桥时抛 `UnsupportedCapability`）：**

- `biometrics` · `bluetooth` · `nfc` · `usb` · `serial` · `midi`
- `contacts` · `calendar` · `printer` · `geolocation`（非 emscripten）

测试或本地演示可 `enable_capability_sim("biometrics", …)` 临时放开。

```python
import asyncio
from echoui.exceptions import UnsupportedCapability
from echoui.platform import clipboard, detect, notifications, share, biometrics

async def demo():
    await clipboard.write_text("hello")
    assert await clipboard.read_text() == "hello"
    await share.share({"title": "EchoUI", "url": "https://example.com"})
    try:
        await biometrics.authenticate("pay")
    except UnsupportedCapability:
        pass

asyncio.run(demo())
notifications.show("Hi", body="there")
assert detect().capabilities
```

## mobile

默认宿主 Python **不**静默成功：`haptics_impact` / `orientation_lock` / `push_register` 无移动壳时抛 `UnsupportedCapability`。  
`enable_mobile_sim()` 仅用于测试/演示日志桥。

## a11y

```python
from echoui.a11y import focus_trap, skip_link

skip_link("#main")
focus_trap(True)
```

## print_view

```python
from echoui import col, print_view, text
from echoui.print import PageStyle, print_styles

col(
    text("screen"),
    print_view(text("仅打印此区域")),
)
print_styles(page=PageStyle(size="A4", margin="1.5cm"))
```

Web emit 含 `.e-print-view` 与 `@media print` CSS；`PageStyle` 生成 `@page` 规则。

## collab — Doc / Awareness

```python
from echoui.collab import Doc, SyncRelay

relay = SyncRelay()
doc = Doc(peer_id="a", relay=relay)
doc.set("title", "Hello")
relay.broadcast(doc.session, "title", "Hello")
doc.set_cursor(10, 20)
doc.awareness.list_peers()
```

生产网络同步见 `echoui[collab]` pycrdt 可选依赖。

## devtools

```bash
echoui devtools main.py
```

输出 signals / reactive bindings 图，便于 compile-local 调试。
