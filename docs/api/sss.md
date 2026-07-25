# SSS 范式（PLAN §1 / §4 / §34）

EchoUI 只有三个概念：**Screen → Stage → Sprite**。一切 UI 都是 Sprite；role 只决定渲染方式，不产生平行类型系统。

## 树结构

```
App
 └── Screen          整页 / 窗口 / 路由（视图表面）
      ├── flow 模式   → Sprite 树（col / row / box / text / button …）
      └── free 模式   → Stage（唯一根）→ Sprite（x,y 坐标）
           └── Sprite（可任意嵌套）
```

## flow Screen（文档 / 表单 / 仪表盘）

```python
class Counter(Screen):
    layout = "flow"  # 默认

    def build(self):
        return col(
            text(lambda: f"Count: {store.count}"),
            button("+1", on_click=inc),
        )
```

`col` / `row` 本身是 **box 角色 Sprite**，由布局引擎排列。flow Screen **不需要** `stage()`。

flow 页面里可以**嵌入** free Stage（PLAN §1.3）：

```python
return col(
    text("Dashboard"),
    stage(MiniMap(), width=320, height=240, layout="free"),
)
```

## free Screen（游戏 / 画布 / 编辑器）

```python
class Game(Screen):
    layout = "free"

    def build(self):
        return stage(
            Player(),
            *enemies,
            HUD(),
            width=640,
            height=360,
            layout="free",
            fill_viewport=True,  # 默认 True：Stage 铺满整个窗口
        )
```

### 必须遵守

1. `build()` **直接** `return stage(...)` — 禁止 `col(stage(), button())`
2. 分数、HUD、按钮都是 **Stage 内的 Sprite**（用 `x` / `y` 定位）
3. `640×360` 是**设计坐标**；`fill_viewport` + `fitStage()` 按窗口缩放（PLAN §4.3）

### 错误示例

```python
# ❌ 违反 SSS — 编译期 SSSError
return col(
    text("Score"),
    stage(...),
    button("Jump"),
)
```

## 编译器

- `echoui/compiler/sss.py` — 分析阶段校验与规范化
- `layout="free"` 的 Screen 若根节点不是单个 `stage`，抛出 `SSSError`
- free Stage 默认 `fill_viewport=True`

## 测试

```bash
pytest tests/unit/test_sss_contract.py -q
```

## 参见

- [PLAN.md](../../.claude/docs/PLAN.md) §1、§4
- [INDEX.md](INDEX.md) — PLAN 对齐摘要
- [08_全量追踪矩阵.md](../../.claude/docs/08_全量追踪矩阵.md)
