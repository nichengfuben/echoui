# @on / echoui build·dev

| 字段 | 内容 |
|------|------|
| 规格域 | events / cli |
| 模块 | `echoui.events`, `echoui.cli` |
| 引入版本 | 0.1.0 |
| 矩阵行 | §10 事件 / §27 编译管线 |

## 最小示例

```bash
echoui new demo
cd demo
echoui build --target web
echoui build --target tui
```

## 测试

- `tests/integration/test_build_web.py`
- `tests/unit/test_compiler.py`
