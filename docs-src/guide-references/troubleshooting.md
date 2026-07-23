# EchoUI 排错指南

> 解释**为什么错**。机器可执行验收见 `.claude/docs/09_验收与闭环协议.md`（仅 agent）。

---

## 反应式：改了数据界面不更新

**现象：** `store.count += 1` 后 Web 上数字不变。

**根因：** 未走 Store/reactive；绑定快照而非 signal；batch 未结束。

```bash
pytest tests/unit/test_reactive.py -q
```

见 [易混淆对照 · Store vs signal](./易混淆对照.md#状态与事件)。

---

## 编译产物白屏或 404

1. 勿用 `file://` 打开 → `python -m http.server -d dist/web`。
2. 查 bundler `base` 与部署路径。
3. 先 `echoui check`。

---

## `echoui dev` 热更新无效

确认 `pip install -e .`、watch 的是项目源码而非 site-packages。

---

## Router guard 死循环

guard 互跳 → 单测覆盖返回值；目标路由上 guard 应返回 `None`。

---

## 逃生层不随 signal 更新

注入脚本未挂 reactive 回调 → `examples/05_escape_layer`。

---

## TUI free 模式异常

终端 free 为栅格降级，属预期；flow 错乱则查 `pip install -e ".[tui]"`。

---

## 文档与矩阵不一致

以代码 + `.claude/docs/08_全量追踪矩阵.md` 为准；改 API 同步 `docs-src/echoui/`。

---

## 仍无法解决

`PROGRESS.md` → [易混淆对照](./易混淆对照.md) → 附 pytest/build 日志与最小 example。
