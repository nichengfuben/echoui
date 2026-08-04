# EchoUI 组件文档

## 组件概览

EchoUI 提供丰富的终端 UI 组件，所有组件支持链式调用和主题配置。

## 核心组件

### ConsoleUI

终端控制台，提供基础输出能力。

```python
from echoui.components.console_ui import ConsoleUI

ui = ConsoleUI(normal_mode=True)
ui.print("Hello").newline().print("World")
```

**注意**: `ConsoleUI.print(text)` 接受参数并立即输出，
与 `EchoUI.print()` 行为完全不同。

### BoxBuilder

框体组件，用于包裹内容并添加标题。

```python
from echoui.components.box_builder import BoxBuilder

box = BoxBuilder(normal_mode=True).title("标题").content("内容").build()
```

- 支持构造函数参数和链式方法两种风格
- `build()` 和 `render()` 等价

### TableBuilder

表格组件，支持表头和数据行。

```python
from echoui.components.table_builder import TableBuilder

table = (
    TableBuilder(normal_mode=True)
    .set_headers(["ID", "Name"])
    .add_row(["1", "Alice"])
    .add_row(["2", "Bob"])
    .render()
)
```

- 仅支持链式方法，不支持构造函数参数

### ProgressBar

进度条组件。

```python
from echoui.components.progress_bar import ProgressBar

bar = ProgressBar(current=75, total=100, message="加载中")
print(bar.render())
```

### Spinner

加载动画组件。

```python
from echoui.components.spinner import Spinner

spinner = Spinner(normal_mode=True)
print(spinner.render())
```

### Notification

通知组件，支持四种类型。

```python
from echoui.components.notification import Notification

Notification(normal_mode=True).success("操作成功").render()
Notification(normal_mode=True).warning("警告信息").render()
Notification(normal_mode=True).error("错误信息").render()
Notification(normal_mode=True).info("提示信息").render()
```

### BlockArt

块字符艺术组件。

```python
from echoui.components.block_art import BlockArt

# 注意: render_text() 设置文本并返回 self，需再调用 .render()
art = BlockArt(text="Hi", normal_mode=True).render()
```

**重要**: `render_text()` 是链式方法，返回 self 而非字符串。

### KeyValueList

键值对列表组件。

```python
from echoui.components.key_value_list import KeyValueList

kvl = KeyValueList().add("名称", "EchoUI").add("版本", "2.0.0").render()
```

**注意**: 构造函数不接受任何参数，通过 `.add(key, value)` 链式添加。

### TreeView

树形结构组件。

```python
from echoui.components.tree_view import TreeView

tree = TreeView(data={"root": {"child1": {}, "child2": {}}}).render()
```

## 高级组件

### EchoUI (主控制器)

统一入口，组合所有常用组件。

```python
from echoui import EchoUI

ui = EchoUI(normal_mode=True)
ui.block("EchoUI").rule("=").success("启动成功").print()
```

### PanelBuilder

面板布局组件（待完善文档）。

### ColumnLayout

列布局组件（待完善文档）。

## CJK 字符处理

**重要**: 多个组件使用 `len()` 计算宽度，对中文会导致布局错位。
应使用 `echoui.utils.text.get_display_width()` 替代。

受影响的组件:
- PanelBuilder
- ColumnLayout
- KeyValueList

## 主题支持

所有组件接受 `theme` 参数，传入 `ThemeConfig` 实例:

```python
from echoui.core.theme import Theme

theme = Theme.get("default")
box = BoxBuilder(theme=theme).title("标题").content("内容").build()
```

## 正常模式

设置 `normal_mode=True` 时，组件输出纯文本而非 ANSI 转义序列，
适用于不支持颜色的终端。
