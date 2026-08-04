# AGENTS.md -- components/ 目录易混淆点

> **活文档**：在此目录工作时更新本文件。
> 父级 AGENTS.md 已记录项目级陷阱，本文件仅记录 components/ 特有的问题。

**最后更新：** 2026-05-16

---

## 必须避免的严重错误

### [CRITICAL] KeyValueList 构造函数不接受任何参数
**你会假设：** KeyValueList(normal_mode=True, theme=cfg) 可以工作
**实际情况：** __init__() 不接受参数，调用 super().__init__() 使用默认值
**犯错后果：** TypeError: KeyValueList.__init__() got an unexpected keyword argument
**正确做法：** KeyValueList() 直接实例化，通过 .add(k, v) 添加内容

### [CRITICAL] StreamWriter 不接受 normal_mode 参数
**你会假设：** 所有组件都接受 normal_mode
**实际情况：** StreamWriter.__init__() 不接受 normal_mode 参数
**犯错后果：** TypeError: unexpected keyword argument 'normal_mode'
**正确做法：** StreamWriter() 直接实例化

### [CRITICAL] ConfirmDialog 只接受 message 参数
**你会假设：** ConfirmDialog(renderer=..., normal_mode=...) 可以工作
**实际情况：** __init__(message: str) 只接受 message
**犯错后果：** TypeError: unexpected keyword argument
**正确做法：** ConfirmDialog(message="确认？")

### [CRITICAL] Countdown.run() 不接受参数
**你会假设：** run(on_tick=callback) 可以传参
**实际情况：** 构造函数接受 seconds= 和 on_tick=，run() 不接受参数
**犯错后果：** TypeError: run() got an unexpected keyword argument
**正确做法：** Countdown(seconds=10, on_tick=cb).run()

---

## 易混淆之处

### [WARNING] BlockArt 有 text() 和 render_text() 两个等价方法
**混淆之处：** 两个方法都做同一件事（设置 self._text）
**澄清：** 它们是别名，render_text() 不执行渲染，只设置文本并返回 self

### [WARNING] BoxBuilder 同时支持构造函数参数和链式方法
**混淆之处：** BoxBuilder(content="hi") 和 BoxBuilder().content("hi") 都有效
**澄清：** TableBuilder 只支持链式方法 set_headers()/add_row()，不支持构造函数传数据

### [WARNING] Notification 实例不可复用
**混淆之处：** n = Notification(); n.success("ok"); n.error("fail") 以为会积累
**实际情况：** 每次调用 success/error/warning/info 都覆盖内部 _prefix 和 _message
**正确做法：** 每个消息创建新 Notification 实例

### [WARNING] PanelBuilder 和 ColumnLayout 使用 len() 计算宽度（待修复）
**混淆之处：** 以为所有组件都用 get_display_width()
**实际情况：** 这两个文件使用 len()，包含中文时布局会错位
**状态：** 已知问题，待修复

---

## 最近发现的意外日志

<!-- 追加新发现 -->
