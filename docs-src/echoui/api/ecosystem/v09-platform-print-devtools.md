# platform / a11y / print / devtools (v0.9)

| 项 | 说明 |
|----|------|
| 规格域 | platform / a11y / print / CLI devtools |
| 状态 | done (Web/桌面内存模拟 + print CSS) |
| 测试 | `test_ecosystem_v09.py` |
| 示例 | `examples/07_full_web`（i18n/a11y 子集） |

## platform — 内存 clipboard / notifications / share

```python
import asyncio
from echoui.platform import clipboard, detect, notifications, share

async def demo():
    await clipboard.write_text("hello")
    assert await clipboard.read_text() == "hello"
    await share.share({"title": "EchoUI", "url": "https://example.com"})

asyncio.run(demo())
notifications.show("Hi", body="there")
assert detect().capabilities
```

桌面 `dialog_open_file` 委托 `files.pick()`（tkinter 原生选文件）。

## a11y

```python
from echoui.a11y import focus_trap, skip_link

skip_link("#main")
focus_trap(True)
```

## print_view

```python
from echoui import col, print_view, text

col(
    text("screen"),
    print_view(text("仅打印此区域")),
)
```

Web emit 含 `.e-print-view` 与 `@media print` CSS。

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
