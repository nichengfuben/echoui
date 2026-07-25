# Signal

| 字段 | 内容 |
|------|------|
| 规格域 | reactive |
| 模块 | `echoui.reactive.Signal` |
| 引入版本 | 0.1.0 |
| 矩阵行 | §9 reactive |

## 一句话

细粒度可变状态容器；订阅者仅在值变化时重跑。

## 签名

```python
class Signal(Generic[T]):
    def __init__(self, value: T) -> None: ...
    @property
    def value(self) -> T: ...
    def set(self, value: T) -> None: ...
```

## 目标支持

| target | 状态 | 说明 |
|--------|------|------|
| web | done | 编译为 runtime signal |
| tui | done | 同核心 |
| desktop/gui | done | 同核心 |

## 行为说明

1. 读 `.value` 时注册当前 computed/effect 依赖。
2. `set` 相等值时不通知。

## 最小示例

```python
from echoui.reactive import Signal

count = Signal(0)
count.set(count.value + 1)
```

## 测试

- `tests/unit/test_reactive.py`
