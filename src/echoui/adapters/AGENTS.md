# AGENTS.md -- adapters/ 目录易混淆点

> **活文档**：在此目录工作时更新本文件。
> 父级 AGENTS.md 已记录项目级陷阱，本文件仅记录 adapters/ 特有的问题。

**最后更新：** 2026-05-16

---

## 必须避免的严重错误

### [CRITICAL] TerminalAdapter 使用已弃用的 asyncio.get_event_loop()
**你会假设：** asyncio.get_event_loop() 在所有 Python 版本中安全
**实际情况：** Python 3.10+ 已弃用，3.12+ 在无运行循环时抛出 RuntimeError
**犯错后果：** 在 Python 3.14（当前环境）中产生 DeprecationWarning
**正确做法：** 在异步上下文中使用 asyncio.get_running_loop()，或保持现状（pragma: no cover）

---

## 易混淆之处

### [WARNING] BaseAdapter.get/post/put/delete 是装饰器工厂
**混淆之处：** 名称暗示是 HTTP 请求方法
**实际情况：** 它们是装饰器工厂，用于注册路由处理函数
**示例：** @adapter.get("/") 注册 GET 路由，不是发送 HTTP 请求

### [WARNING] TerminalAdapter 仅有终端能力
**混淆之处：** 以为 adapters/ 包含 Web/桌面适配器
**实际情况：** 目前只有 TerminalAdapter，Web/桌面适配器仅架构预留
**正确做法：** 需要 Web 能力时创建 aiohttp_adapter.py 等

---

## 最近发现的意外日志

<!-- 追加新发现 -->
