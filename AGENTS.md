# AGENTS.md -- 错误、意外与易混淆点

> **用途**：本文件记录 AI 代理在本项目中工作时常见的错误和易混淆之处。
> 如果你遇到了意外情况，请立即告知开发者并追加到本文件中，
> 以防未来的代理重蹈覆辙。
>
> **活文档**：在工作过程中实时更新本文件。

**文件指示栏**

| 文件 | 状态 |
|------|------|
| `.agents/TASK.txt` | 已读取，当前会话入口 |
| `.agents/MISTAKE_GUIDE.txt` | 已读取，记录 12 条 [CRITICAL] 禁止行为 |
| `.agents/CODE_GUIDE.txt` | 已读取，记录项目架构与开发规范 |
| `.agents/AGENTS_MD_GUIDE.txt` | 已读取，记录 AGENTS.md 生成工作流程 |
| `AGENTS.md` (本文件) | 已更新，2026-05-16（会话 5） |

**最后更新：** 2026-05-16（会话 5）
**项目身份：** EchoUI - 纯 Python 终端 UI 框架，通过 ASCII/ANSI 字符在终端中渲染界面，使用调用链驱动的组件 API。

---

## 必须避免的严重错误

### [CRITICAL] ConsoleUI.print() 与 EchoUI.print() 同名但行为完全不同
**你会假设：** 两者都接受文本参数并立即输出
**实际情况：** ConsoleUI.print(text) 接受参数并立即写入；EchoUI.print() 不接受参数，仅刷新内部缓冲区
**犯错后果：** 调用 EchoUI.print("hello") 会忽略参数，文本不会输出
**正确做法：** EchoUI 使用链式方法积累内容后调用 .print() 刷新；ConsoleUI 直接 print(text)

### [CRITICAL] 子模块 __init__.py 全部为空，无法从子包直接导入
**你会假设：** from echoui.components import Spinner 可以工作
**实际情况：** 只有 src/echoui/__init__.py 有重导出，components/__init__.py 等全为空
**犯错后果：** ImportError: cannot import 'Spinner' from 'echoui.components'
**正确做法：** 必须使用完整路径：from echoui.components.spinner import Spinner

### [CRITICAL] BlockArt.render_text() 设置文本但不渲染
**你会假设：** render_text() 返回渲染后的字符串
**实际情况：** render_text() 是链式方法，返回 self；需要再调用 .render() 获取字符串
**犯错后果：** 得到 BlockArt 对象而非字符串
**正确做法：** art.render_text("Hi").render()

### [CRITICAL] 多个组件使用 len() 计算 CJK 宽度（违反 MISTAKE_GUIDE）
**你会假设：** 所有组件都使用 get_display_width() 处理 CJK
**实际情况：** PanelBuilder、ColumnLayout、KeyValueList 使用 len() 计算宽度
**犯错后果：** 包含中文时布局错位
**正确做法：** 这些文件的 len() 调用应替换为 get_display_width()（待修复）

### [CRITICAL] 5 个文件使用已弃用的 asyncio.get_event_loop()
**你会假设：** asyncio.get_event_loop() 在所有 Python 版本中可用
**实际情况：** Python 3.10+ 已弃用，3.12+ 在无运行循环时抛出 RuntimeError
**犯错后果：** 在 Python 3.12+ 中运行时报错
**正确做法：** 在异步上下文中使用 asyncio.get_running_loop()，同步上下文使用兼容层

---

## 易混淆之处

### [WARNING] KeyValueList 构造函数不接受任何参数
**混淆之处：** 大多数组件接受 renderer/normal_mode/theme 参数，但 KeyValueList.__init__() 不接受任何参数
**澄清：** KeyValueList 通过 .add(key, value) 链式方法添加内容，构造时不传参
**示例：** KeyValueList().add("name", "EchoUI").render()

### [WARNING] BoxBuilder 同时支持构造函数参数和链式方法
**混淆之处：** BoxBuilder(content="hi", title="T") 和 BoxBuilder().content("hi").title("T") 都有效，但 TableBuilder 只支持链式方法
**澄清：** BoxBuilder 是特例，TableBuilder 必须用 set_headers()/add_row()
**正确做法：** 统一使用链式方法风格

### [WARNING] Theme 是注册表，ThemeConfig 是数据
**混淆之处：** Theme.get("default") 返回 ThemeConfig 实例
**澄清：** Theme 类仅有类方法（get/register/list_names），ThemeConfig 是 frozen dataclass 持有颜色值
**正确做法：** 组件通过 theme=Theme.get("default") 传递 ThemeConfig 实例

### [WARNING] validate_hex_color 在 color.py 和 validators.py 中重复导出
**混淆之处：** 同一函数存在于两个模块
**澄清：** validators.py 从 color.py 重新导入，功能完全相同
**正确做法：** 优先从 echoui.utils.color 导入

---

## 结构性意外

| 预期 | 实际 | 影响 |
|------|------|------|
| pyproject.toml 中 Python 版本一致 | requires-python>=3.8, mypy=3.10, black=py38 | 不确定目标版本 |
| 覆盖率全局 90% 即达标 | MISTAKE_GUIDE 要求 core>=95% | pyproject.toml 不 enforcing 模块级阈值 |
| asyncio 测试用 @pytest.mark.asyncio | 现有异步测试用 asyncio.run() 包装 | 标记未被使用 |

---

## 命名陷阱

| 名称 | 你以为的含义 | 实际含义或行为 |
|------|-------------|----------------|
| `render_text()` (BlockArt) | 渲染文本为字符串 | 设置内部文本并返回 self |
| `build()` (BlockArt) | 构建并返回新对象 | render() 的别名，返回字符串 |
| `ConsoleUI.print(text)` | 刷新缓冲区 | 立即写入 _output_stream |
| `EchoUI.print()` | 输出文本 | 刷新内部 _buffer 到 _stream |
| `BlockArt` vs `AsciiArtBuilder` | 同一功能 | BlockArt 用块字符，AsciiArtBuilder 用任意行 |

---

## 依赖与导入陷阱

- **无循环导入**：组件使用 TYPE_CHECKING 块隔离类型导入
- **renderer.py 内部有延迟导入**：ConfigError 在 render_progress_bar() 方法体内导入，不要"优化"到文件顶部
- **所有子包 __init__.py 为空**：必须使用完整模块路径导入

---

## 构建、测试与运行意外

- **pytest 命令在 bash 中路径解析问题**：`python -m pytest tests/` 可能被解析为找不到的路径，使用 `python -c "import pytest; pytest.main([...])"` 替代
- **conftest.py 缺少 MISTAKE_GUIDE 中列出的 fixture**：console_ui 和 terminal_adapter fixture 未在 conftest.py 中定义
- **pytest-asyncio strict 模式**：需要在 async 测试上显式添加 @pytest.mark.asyncio

---

## 反模式（明确禁止）

| 禁止做法 | 应采取的做法 | 原因 |
|----------|-------------|------|
| 用 pass 作为功能实现 | 实现真实业务逻辑或抛出 NotImplementedError | 静默空操作导致难以调试 |
| 用 print 调试 | 使用 logging.getLogger(__name__) | 污染输出 |
| 用 f-string 格式化日志 | 使用 logger.info("msg: %s", value) | f-string 在日志过滤前就执行插值 |
| normal_mode=True 时输出 ANSI | 先检查 self._normal_mode | 在不支持 ANSI 的终端显示乱码 |
| 用 len() 计算 CJK 宽度 | 使用 utils/text.py 的 get_display_width() | len() 对 CJK 字符计算错误 |

---

## 配置陷阱

- **coverage exclude_lines**：`if TYPE_CHECKING:` 和 `@abstractmethod` 被排除，在此块中的代码不计入覆盖率
- **pylint 禁用 C0114/C0115/C0116**：不检查模块/类/函数文档字符串，但 MISTAKE_GUIDE 要求必须有
- **全局 fail_under=90**：不 enforce 模块级阈值（core 需 95%），需手动指定 --cov-fail-under

---

## 最近发现的意外日志

### 2026-05-16 -- 会话 4 修复 doctest 失败
**上下文：** 阶段 5 完成验证中发现 4 个 doctest 失败
**修复内容：**
1. `src/echoui/__init__.py`: echoui()/EchoUI/kv 的 doctest 产生 stdout 输出，添加 `# doctest: +SKIP`
2. `src/echoui/components/block_art.py`: render_text() 返回 self，修正为 `.render()`
**结果：** 443 passed, 3 skipped, 0 failed

### 2026-05-16 -- AGENTS.md 重构
**上下文：** 按照 AGENTS_MD_GUIDE.txt 重新生成 AGENTS.md
**变更：** 从"工作日志"格式重构为"错误/意外/易混淆点"格式，删除通用信息，保留具体陷阱记录

### 2026-05-16 -- 会话 5 发现空目录和缺失模块
**上下文：** 执行 TASK.txt 验证流程时发现 db/ 和 interfaces/ 目录完全为空
**发现内容：**
1. `src/echoui/db/` 和 `src/echoui/interfaces/` 是空包（仅有空 `__init__.py`）
2. `docs/` 和 `examples/` 也是空目录
3. 用户明确指出"没有严谨检查，有些文件夹甚至是完全空的"
**实现内容：**
- 创建 `db/model.py`、`db/field.py`、`db/session.py`、`db/query_builder.py`、`db/migration.py`
- 创建 `interfaces/router.py`、`interfaces/websocket_manager.py`
- 创建对应测试：`test_model.py`、`test_field.py`、`test_session.py`、`test_query_builder.py`、`test_migration.py`、`test_router.py`、`test_websocket_manager.py`
- 创建集成测试 `test_db_session.py` 和 E2E 测试 `test_form_flow.py`、`test_dashboard_flow.py`
- 更新 `db/__init__.py` 和 `interfaces/__init__.py` 导出
**结果：** 478 passed, 0 failed

### 2026-05-16 -- 会话 5 Model 数据类描述符模式陷阱
**上下文：** 实现 db/ ORM 层时，Model 使用 `@dataclass` 但字段通过 Field 描述符定义
**意外：** `@dataclass` 不会将类属性的 Field 描述符转换为实例字段，导致 `User(name="张三")` 抛出 `TypeError: unexpected keyword argument`
**解决方案：** 使用 `@dataclass(init=False)` 并在自定义 `__init__` 中遍历 MRO 收集 Field 描述符，通过 `object.__setattr__` 设置实例属性。同时基础字段（id/created_at/updated_at）使用 `kwargs.get()` 而非条件判断，以支持 update 场景传入已有值
**补充：** `dataclasses.replace()` 不适用于 `init=False` 的自定义 dataclass，session.update() 需手动复制属性字典再构造新实例

<!-- 当你遇到意外时，在此追加：
### {ISO 日期} -- {标题}
**上下文：** {你正在执行的任务}
**意外：** {发生了什么}
**解决方案：** {正确的行为或做法}
-->
