# data / forms / i18n / collab

| 项 | 说明 |
|----|------|
| 规格域 | data / forms / i18n / collab |
| 状态 | done (Web/Python API) |
| 测试 | `test_data_i18n_forms.py`, `test_collab_sync.py`, `test_ecosystem_v09.py` |
| 示例 | `examples/07_full_web`, `09_full` |

## forms — 文件校验 / 异步校验

```python
from echoui.forms import Form, field, file_size, file_type, max_files

f = Form().add(field("img", file_size(1024), file_type("image/"), max_files(2)))
f.validate({"img": {"size": 512, "type": "image/png"}})

# 协程校验器：同步 validate 会跳过；用 validate_async
async def unique(value, _data):
    return "taken" if value == "x" else None

f2 = Form().add(field("name", unique))
await f2.validate_async({"name": "x"})  # errors["name"] == "taken"
```

```python
from echoui.api import ApiClient, chunk_ranges

# 纯范围规划（无网络）
assert chunk_ranges(16, 5) == [(0, 4), (5, 9), (10, 14), (15, 15)]

# 顺序分块上传：Content-Range + X-Chunk-Index/Count；on_progress(sent, total)
client = ApiClient(base_url="http://127.0.0.1:8080")
await client.upload_chunked("/up", b"...", chunk_size=256 * 1024, on_progress=print)
```

诚实边界：`upload_chunked` 为顺序 multipart 子集（非 tus/断点续传协议）；服务端错误映射深度仍浅。

## router — lazy / 嵌套 layout

```python
from echoui.router import Router

r = Router()
r.add("/", "Home", layout="Root")
app = r.group("/app", layout="AppShell")
app.add("/", "AppHome")
app.add("/settings", "Settings", layout="SettingsPane")
r.add("/app/profile", "Profile", layout="ProfilePane", parent="/app")
r.add("/app", "AppIndex", layout="AppShell")

r.navigate("/app/settings")
assert r.current_layouts() == ["AppShell", "SettingsPane"]
assert r.current_layout() == "SettingsPane"
```

诚实边界：`group`/`parent`/`current_layouts` 已验；深嵌套 layout 组件树与编译期 layout 槽仍浅。

## data — 虚拟列表 / 表格

```python
from echoui.data import DataTable, Tree, TreeNode, VirtualList

vl = VirtualList(items=range(1000), item_height=24, viewport_height=240)
vl.scroll_to(50)
dt = DataTable(columns=[{"key": "n"}], rows=[{"n": 2}, {"n": 1}])
dt.sort_by("n")
```

Web emit：`virtual_list` 带 `.e-virtual-viewport`；`gestures.js` 接线滚动。

## i18n

```python
from echoui.i18n import t, plural, set_locale, load_catalog, load_plural
```

## collab

`Doc` / `Presence` / `Awareness` + `SyncRelay` LWW 广播（内存/测试）；pycrdt 见 `echoui[collab]`。详见 [v09-platform-print-devtools.md](v09-platform-print-devtools.md)。
