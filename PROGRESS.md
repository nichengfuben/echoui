# EchoUI Progress

> **审计规则**：仅 `[x]` 表示本机命令验证通过；`[ ]` 未完成。  
> **唯一真相来源**：本文件 + `08_全量追踪矩阵.md`。

## 当前阶段

**v1.2.0 — 媒体/上传/音频实装**（2026-07-25 进行中）

PyPI 1.0.1 已发；1.2.0 本地 build 完成，待 push。

---

## 09 协议 — 机器可检查项

| 项 | 状态 | 证据 |
|----|:----:|------|
| `pip install echoui` | [x] | PyPI 1.0.1；本地 1.2.0 whl |
| `pytest -q` | [x] | 112 passed |
| `mypy echoui` | [x] | 84 files |
| `ruff check echoui tests` | [x] | 全绿 |
| `python achecker.py` | [x] | 全绿 |
| `python -m build` + `twine check` | [x] | 1.0.1 PASSED |
| `echoui new` + `build --target web` | [x] | pip workflow 测 |
| `echoui build --target tui` 真实 UI | [ ] | 仅通用 Textual 壳 |
| Desktop `.exe` 本机验证 | [ ] | 未产出/未验 |
| Android `.apk` 本机验证 | [ ] | 未验 |
| iOS CI artifact 绿 | [ ] | workflow 存在，未确认跑通 |
| 08 矩阵终态（无 stub 冒充 done） | [ ] | 见矩阵 v2 |

---

## 已真实闭环（可验证，非全 PLAN）

| 域 | 状态 | 证据 |
|----|:----:|------|
| compile-local Web 架构 | [x] | validate_local + core.js 本地帧/事件 |
| SSS Web 编译 | [x] | 八示例 web build |
| 反应式 Signal/Store | [x] | test_reactive, test_web_reactive |
| 路由静态多屏 | [x] | 04 示例 + test_router_nav |
| 逃生层 raw.js | [x] | 05_escape_layer + test_escape |
| Chart.js / MapLibre emit | [x] | 07_full_web |
| HTML5 video/audio 标签 | [x] | 08_media |
| CLI 脚手架 | [x] | echoui new / dev / build |
| 源码禁词检查 | [x] | check_banned_terms.py |
| PyPI 发布 | [x] | 1.0.1 已上传 |

---

## 未完成 — 全量 TODO（按优先级）

### P0 — 用户可见缺口

- [x] `file_input(accept="image/*")` + Web emit + change→Signal
- [x] `image(src=signal)` 响应式 src 绑定
- [x] `echoui.audio.play()` Web Audio 封装（compile-local）
- [x] 跑酷示例：背景图 + 角色贴图 + 跳跃音效
- [x] overlay modal/drawer Web 渲染

### P1 — PLAN §11–§21 Web 枚举

- [ ] 表单 file 校验 + 上传进度 + api.upload 接线
- [ ] storage.files.pick/save（Web OPFS 桥接 Python API）
- [ ] platform web 子集：clipboard / notifications（UnsupportedCapability  elsewhere）
- [ ] 50+ role 的 Web emit 补齐（textarea/select/checkbox/file…）
- [ ] 动画/手势 Web pointer 事件接线

### P2 — 多端 A 类（00_MASTER / 06 阶段）

- [ ] TUI：IR→Textual 真实渲染（非 Static 壳）
- [ ] Desktop：Qt 全 role 子集 + PyInstaller .exe 本机验
- [ ] Android：Gradle APK 本机验
- [ ] iOS：Actions 跑通 + artifact 下载验证

### P3 — 生态闭环（07 + 09）

- [ ] docs-src API 图鉴：50+ role 四件套
- [ ] collab：pycrdt 或网络同步
- [ ] data：VirtualList/DataTable 虚拟滚动
- [ ] i18n：plural/format_* 
- [ ] a11y_audit 扩展规则
- [ ] Playwright escape+signal 集成测

### P4 — 空壳模块填实或标 interface-only

- [x] audio / media / desktop / mobile / rtc / graphql / rpc / three（基础 API 已实装）

---

## 诚实边界（C 类 / OS 限制）

| 项 | 状态 | 说明 |
|----|:----:|------|
| iOS 本地 Xcode 构建 | [ ] | Windows 物理限制；靠 CI |
| 应用商店签名上架 | [ ] | 需开发者账号 |
| box2d-py | — | 已换 pymunk extra（1.0.1） |

---

## 审计日志

```
2026-07-25 诚实复审计：撤回终态宣称；08 矩阵 v2；PROGRESS 全量 TODO 重置
2026-07-25 PyPI 1.0.1：physics extra pymunk；GitHub release v1.0.1
2026-07-25 PyPI 1.0.0 上传成功；GitHub v1.0.0 release
2026-07-25 compile-local Web + 107 pytest（此前误标终态）
```
