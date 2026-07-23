# EchoUI API 图鉴 —— 条目模板

> 每个对外 API、role 或 CLI 子命令各占一篇。标 `done` 须齐四件套：**实现 + 单测 + example + 本模板**（矩阵见 `.claude/docs/08_全量追踪矩阵.md`，仅 agent 侧）。

建议路径：`docs-src/echoui/api/<模块>/<名称>.md`。

---

## 模板

```markdown
# <API 名称>

| 字段 | 内容 |
|------|------|
| 规格域 | reactive / layout / compiler / … |
| 模块 | `echoui.xxx` |
| 引入版本 | 0.1.x |
| 矩阵行 | 主表或 role 子表标识 |

## 一句话

<做什么、不做什么。>

## 签名

​```python
# 真实签名
​```

## 目标支持

| target | 状态 | 说明 |
|--------|------|------|
| web | done / done-degraded / interface-only / n/a | |

## 行为说明

1. 正常路径
2. 边界与降级

## 前置条件

- **requires:** 权限、extra、工具链
- **limits:** 配额与性能上限

## 最小示例

​```python
# 对应 examples/ 或 tests/
​```

## 常见误用

- **误用 / 后果 / 应改为**

## 易混淆

- 与 **X** 的区别 → [易混淆对照](../易混淆对照.md)

## 测试

- `tests/.../test_<case>.py`
```

---

## v0.1 优先条目

| 优先级 | 条目 | 示例 |
|--------|------|------|
| P0 | Signal / effect / batch | `examples/02_counter` |
| P0 | App / Screen / Sprite | `examples/02_counter` |
| P0 | text / button / box / input | `examples/02_counter` |
| P1 | row / col / style | 同上 |
| P1 | @on / echoui build·dev | tests / CLI |

索引占位：`docs-src/echoui/api/v0.1-index.md`。

---

## 四件套

```
[x] 代码  [x] 单测  [x] example  [x] docs-src 图鉴条目
```

缺一最高 `done-degraded`。
