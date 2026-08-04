# AGENTS.md -- tests/ 目录易混淆点

> **活文档**：在此目录工作时更新本文件。
> 父级 AGENTS.md 已记录项目级陷阱，本文件仅记录 tests/ 特有的问题。

**最后更新：** 2026-05-16

---

## 必须避免的严重错误

### [CRITICAL] conftest.py 缺少 MISTAKE_GUIDE 中列出的 fixture
**你会假设：** console_ui 和 terminal_adapter fixture 可直接使用
**实际情况：** tests/conftest.py 仅定义 event_loop, normal_renderer, gradient_renderer, default_theme, ocean_theme
**犯错后果：** pytest 报错 fixture not found
**正确做法：** 在测试文件中自行创建实例，或扩展 conftest.py 添加缺失 fixture

### [CRITICAL] TerminalAdapter 有两份测试文件
**你会假设：** tests/unit/components/test_terminal_adapter.py 是唯一的测试
**实际情况：** tests/integration/test_terminal_adapter.py 也有测试
**犯错后果：** 修改一份而忘记同步修改另一份
**正确做法：** unit/ 测试适配器的逻辑，integration/ 测试端到行为

---

## 易混淆之处

### [WARNING] pytest 命令在 bash 中路径解析问题
**混淆之处：** python -m pytest tests/ 报 "file or directory not found: 2"
**澄清：** bash 工具对 / 字符有特殊处理
**正确做法：** 使用 python -c "import pytest; pytest.main(['tests/', '-q'])"

### [WARNING] test_base_adapter.py 使用 Dummy 具体子类含 pass
**混淆之处：** MISTAKE_GUIDE 禁止 pass，但此测试文件中有 pass
**澄清：** 抽象方法测试中 pass 是合法的（用于验证抽象机制）
**正确做法：** 保持现状，这是 CRITICAL-001 的合法例外

### [WARNING] test_renderer.py 对 None 颜色期望 (ConfigError, TypeError)
**混淆之处：** 测试期望两种异常类型
**澄清：** None 传入 str 参数会先触发 TypeError，然后才是 ConfigError
**正确做法：** 保持双异常期望，不要"修复"为只期望 ConfigError

### [WARNING] 异步测试未使用 @pytest.mark.asyncio
**混淆之处：** MISTAKE_GUIDE 要求所有 async 测试加此标记
**实际情况：** 现有异步测试用 asyncio.run() 包装
**正确做法：** 新测试使用 @pytest.mark.asyncio，现有测试保持不变

---

## 最近发现的意外日志

<!-- 追加新发现 -->
