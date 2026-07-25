# data / forms / i18n / collab

| 项 | 说明 |
|----|------|
| 规格域 | data / forms / i18n / collab |
| 状态 | done (Web/Python API) |
| 测试 | `test_data_i18n_forms.py`, `test_collab_sync.py`, `test_ecosystem_v09.py` |
| 示例 | `examples/07_full_web`, `09_full` |

## forms — 文件校验

```python
from echoui.forms import Form, field, file_size, file_type, max_files

f = Form().add(field("img", file_size(1024), file_type("image/"), max_files(2)))
f.validate({"img": {"size": 512, "type": "image/png"}})
```

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
