# 内建 Roles

`echoui.roles.ROLE_MAP` 当前映射：

| role | 原生标签 |
|------|----------|
| text | span |
| heading | h1 |
| paragraph | p |
| button | button |
| image | img |
| input | input |
| box / scroll / spacer | div |
| divider | hr |
| link | a |
| screen / stage | div |
| canvas | canvas |

扩展：

```python
from echoui.roles import register_role, register_role_renderer

register_role("badge", "span")
```

完整 role 子表追踪见 `.claude/docs/08_全量追踪矩阵.md`；v0.9 以核心 layout + 表单 role 为主，高级 role 通过 escape 或插件补齐。
