# echoui 包文档镜像

**源路径：** `echoui/`

## 职责

Screen–Stage–Sprite 范式、反应式核心、编译到多 target 的 Python UI 框架。

## 关键入口

| 模块 | 说明 |
|------|------|
| `reactive.py` | Signal、Computed、effect、batch |
| `state.py` / `signals.py` | Store 与事件总线 |
| `sprite.py` / `screen.py` / `stage.py` | SSS 基类与 IR |
| `layout.py` / `style.py` / `roles.py` | 布局、样式、role 注册 |
| `compiler/` | IR 构建、降级、Web 发射、bundler |
| `app.py` / `cli.py` | 应用根与 CLI |

## API 图鉴

- 索引：`docs-src/echoui/api/v0.1-index.md`
- 模板：`docs-src/guide-references/API_图鉴模板.md`

## 约束

- 无虚拟 DOM；客户端不跑 Python。
- 模块 docstring 一句话职责，禁止引用内部规格文件名（见 `code-guide.md`）。
