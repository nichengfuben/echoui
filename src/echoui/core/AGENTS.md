# AGENTS.md -- core/ 目录易混淆点

> **活文档**：在此目录工作时更新本文件。
> 父级 AGENTS.md 已记录项目级陷阱，本文件仅记录 core/ 特有的问题。

**最后更新：** 2026-05-16

---

## 必须避免的严重错误

### [CRITICAL] renderer.py 中 ConfigError 在方法体内延迟导入
**你会假设：** 可以把 from echoui.core.exceptions import ConfigError 移到文件顶部
**实际情况：** render_progress_bar() 方法体内有 from echoui.core.exceptions import ConfigError
**犯错后果：** 移动到顶部可能引起循环导入
**正确做法：** 保持现有延迟导入位置

### [CRITICAL] Theme._registry 是全局 ClassVar，测试会互相污染
**你会假设：** 每个测试的主题注册是隔离的
**实际情况：** Theme._registry 是类级别字典，注册后永久存在
**犯错后果：** 测试 A 注册的主题影响测试 B
**正确做法：** 测试中使用已存在的内置主题，避免注册新主题；或实现 Theme.clear() 并在 teardown 中调用

---

## 易混淆之处

### [WARNING] resolve_breakpoint() 返回 BreakpointConfig，不是 Breakpoint
**混淆之处：** 函数名暗示返回 Breakpoint 枚举
**澄清：** 返回 BreakpointConfig 实例，其 .name 属性才是 Breakpoint 枚举
**示例：** config = resolve_breakpoint(800); config.name 是 Breakpoint.XL

### [WARNING] FluidTypeScale.compute_px() 和 SpacingScale.compute_px() 是实例方法
**混淆之处：** 名称暗示可能是模块级函数
**澄清：** 必须先实例化 TYPE_SCALE_MAP 或 SPACING_MAP 中的配置，再调用 compute_px(viewport_width)

### [WARNING] EventBus.unsubscribe() 需要精确匹配 handler 引用
**混淆之处：** 传入 lambda 或包装函数无法 unsubscribe
**澄清：** 必须保存原始 handler 引用并传入相同的引用

---

## 最近发现的意外日志

<!-- 追加新发现 -->
