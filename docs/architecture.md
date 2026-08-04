# EchoUI 架构文档

## 概述

EchoUI 是一个纯 Python 终端 UI 框架，通过 ASCII/ANSI 字符在终端中渲染界面。
采用调用链驱动的组件 API 设计，支持 Python 3.8-3.14。

## 架构分层

```
┌──────────────────────────────────────────────┐
│                  应用层                       │
│         (用户代码 / 示例 / 演示)               │
├──────────────────────────────────────────────┤
│                  接口层                       │
│      Router / WebSocketManager               │
├──────────────────────────────────────────────┤
│                  适配器层                     │
│  TerminalAdapter / AiohttpAdapter / etc.     │
├──────────────────────────────────────────────┤
│                  组件层                       │
│  ConsoleUI / BoxBuilder / TableBuilder /     │
│  ProgressBar / Spinner / Notification / ...  │
├──────────────────────────────────────────────┤
│                  核心层                       │
│  GradientRenderer / Theme / State / EventBus │
├──────────────────────────────────────────────┤
│                  工具层                       │
│  color.py / text.py / path_utils.py /        │
│  compat.py / validators.py                   │
└──────────────────────────────────────────────┘
```

## 核心设计原则

### 1. 不可变数据模式
- ThemeConfig 使用 frozen dataclass
- Model.update() 返回新对象而非修改原对象
- 状态变更通过 State 容器管理

### 2. 链式 API
- 组件通过方法返回 self 支持链式调用
- 例: `BoxBuilder().title("T").content("C").build()`
- 例: `QueryBuilder(User).where(...).limit(10).find_all(session)`

### 3. 主题系统
- Theme 是注册表，通过 get/register/list_names 管理
- ThemeConfig 是冻结的数据对象，持有颜色值
- 组件通过 `theme=Theme.get("default")` 获取配置

### 4. 跨版本兼容
- Python 3.8-3.14 统一支持
- 使用 `from __future__ import annotations` 延迟求值
- 异步通过 asyncio.run() 包装，不依赖 pytest-asyncio

## 目录结构

```
src/echoui/
├── core/          # 渲染器、主题、状态、事件总线
├── components/    # UI 组件（框体、表格、进度条等）
├── adapters/      # 终端/Web/桌面适配器
├── interfaces/    # 路由和 WebSocket 管理
├── db/            # ORM 层（Model, Field, Session）
├── utils/         # 工具函数（颜色、文本、路径、兼容）
└── ha/            # 高可用服务管理
```

## 测试策略

- 单元测试: `tests/unit/` - 测试单个模块功能
- 集成测试: `tests/integration/` - 测试模块间协作
- E2E 测试: `tests/e2e/` - 测试完整用户流程

覆盖率要求:
- core >= 95%
- components >= 90%
- utils >= 90%
- adapters >= 80%
- 整体 >= 90%
