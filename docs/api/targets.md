# 渲染目标能力矩阵

| 能力 | web | static | tui | desktop | gui |
|------|:---:|:------:|:---:|:-------:|:---:|
| Screen / Stage / Sprite | ✓ | ✓ | ✓ | ✓ | ✓ |
| 反应式 Store | ✓ | ✓ | ✓ | ✓ | ✓ |
| 路由 | ✓ | — | ✓ | ✓ | ✓ |
| HTTP 客户端 | ✓ | — | — | ✓ | ✓ |
| 表单校验 | ✓ | ✓ | ✓ | ✓ | ✓ |
| SSR | ✓ | — | — | — | — |
| 逃生层 raw.js/html | ✓ | ✓ | — | — | — |
| PySide6 桌面 | — | — | — | ✓ | ✓ |

说明：

- **desktop / gui** 需要 `pip install echoui[desktop]` 或 `[gui]`（PySide6）。
- **web sqlite** 为 interface-only：浏览器 OPFS 后端在 Python 侧抛出 `NotImplementedError`，见 `echoui/storage`。
- 不支持的平台能力应通过 `UnsupportedCapability` 或文档标注的降级路径处理。
