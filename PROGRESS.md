# EchoUI Progress

> **审计规则**：仅 `[x]` 表示本机命令验证通过。  
> **重审日期**：2026-07-25 — 对照 PLAN.md §0–35 + 00–09 子规范全量重审后**清空旧勾选**，按代码现实重建。  
> **续更**：同日 media/rtc/FLIP + ws/sse 传输验证后更新勾选（仍不宣称 PLAN 字面 100%）。

## 当前阶段

**重审后重建 — 诚实 partial 基线 + gap-batch + media/rtc/FLIP + physics/tmx/IME/DnD + drop IR/forms async/router lazy/RTL + TMX base64 + nested layouts + object layers + chunked upload**（2026-07-25）

PyPI 包版本 **1.2.13** 仍可安装；**不宣称 PLAN 字面 100%**。  
机器门禁（ruff / mypy / pytest / achecker）以本文件「09 协议」表为准。

---

## 总判断（09 三无遗漏）

| 维度 | 状态 | 说明 |
|------|:----:|------|
| 结构无遗漏 | partial | PLAN 各节在 `echoui/` 有落点；部分为 stub |
| 验证无遗漏 | partial | done/已验子集有测；大量 interface-only 仅表面测 |
| 诚实无遗漏 | partial | 旧夸大勾选已清；README 能力矩阵 + 08 **v12** 已对齐代码 |

---

## 09 协议 — 机器可检查项（仅门禁，不代表能力 done）

| 项 | 状态 | 证据 |
|----|:----:|------|
| `ruff check .` | [x] | 以最近一次绿为准 |
| `mypy echoui` | [x] | 92 files Success |
| `pytest -q` | [x] | **214** passed, 1 skipped（2026-07-25 TMX object layers + upload_chunked） |
| `python achecker.py` | [x] | 0 violations |
| `python -m build` + twine | [x] | `echoui-1.2.13` sdist/wheel + `twine check` PASSED |
| PyPI install 当前线 | [x] | 历史 1.2.13；能力不等于 PLAN 闭环 |
| 08 矩阵无 not-started | [x] | 每节有落点标记 |
| done 项四件套齐 | [ ] | 仅 §9 反应式等少数达标 |

---

## PLAN §0–35 对齐（重审摘要 · gap-batch 后）

| 节 | 主题 | 状态 | 一句话 |
|---|------|:----:|--------|
| 0 | 通用性纲领 | interface-only | 叙述；escape 深度未证 |
| 1 | SSS 范式 | partial | Screen/Stage/Sprite 有；free 坐标细节不全 |
| 2 | 架构 | partial | Web 编译链路真；非 Web 多为壳 |
| 3 | 性能模型 | partial | Signal 细粒度真；SSR~0 / GPU 批未证 |
| 4 | App/Screen/Stage/Camera | partial | **shake 衰减 / zoom_to(duration) / deadzone 已验** |
| 5 | Sprite / MotionChain | partial | **`.then_` 属性链已接**；costume/motion 有 |
| 6 | 内建 roles | partial→done(web emit) | 82 role web emit + 测试；重 role 多为占位 |
| 7 | 布局 | partial | **container queries + rtl/ltr/safe_area CSS 助手已验**；完整 a11y/RTL 布局语义仍浅 |
| 8 | 样式 | partial | style/theme/scoped/dark 有；**rtl/safe_area/writing_mode 已验**；具名 scheme 弱 |
| 9 | 反应式 | **done** | Signal/Computed/Effect/Store/batch/untrack + 测 |
| 10 | 事件/输入 | partial | key/mouse/frame；**IME + 文件 DnD + drop_targets IR→client_cfg 已验**；gamepad 弱 |
| 11 | 表单 | partial | validators 真；**validate_async 已验**；**upload_chunked + progress 已验**（非 tus） |
| 12 | 存储 | partial | **FileBackend + configure_storage + Cookie max_age 已验**；默认仍可内存 |
| 13 | 网络 | partial | REST/query 真；**api.ws/sse 工厂+aiohttp live 传输已验**；**upload_chunked 已验**；rtc 进程内 partial |
| 14 | 路由 | partial | match/guard/middleware 真；**lazy + group/parent + current_layouts 已验**；深嵌套 layout 组件树仍浅 |
| 15 | 异步/并发 | partial | **workers ThreadPool 已验**；tasks schedule/tick_minute 已验；wasm 弱 |
| 16 | 动画/手势 | partial | tween/spring + 具名 easing + **FLIP API 已验**；列表 emit 接线有限 |
| 17 | 游戏 | partial | clone/A*；**AABB + 可选 pymunk + TMX CSV/base64(+gzip/zlib) + object layer 点/矩形/gid + astar_on_tilemap 已验**；非完整 Box2D；无 infinite/zstd/完整 polygon |
| 18 | 绘图 | partial | **canvas fluent ctx 已验**；three interface-only |
| 19 | 媒体 | partial | audio 队列；**camera/geo/screen/sensors 诚实 sim**；非真设备桥 |
| 20 | 平台 API | partial | **宿主内存桥保留**；硬件 API **UnsupportedCapability**；mobile 不再静默 pass |
| 21 | Overlay | partial | modal/drawer IR+CSS；toast 内存列表 |
| 22 | 数据展示 | partial | **VirtualList → role virtual_list + web emit 已验**（窗口化仍 compile 切片） |
| 23 | i18n/a11y/print | partial | t/plural/a11y_audit 真；**PageStyle/print_styles 已验** |
| 24 | collab | partial | LWW/pycrdt 真；**默认进程内 relay** |
| 25 | 逃生层 | partial | raw.js/html/css + Playwright；native/ffi 抛错 |
| 26 | 多端 | partial | web/static **done**；**gui lowered.json + render_qt_tree 已验**；tui/desktop/android/ios 仍壳为主 |
| 27 | 编译管线 | partial | web parse→emit 闭环；他端复用 lower_web |
| 28 | 插件 | partial | 装饰器+示例；自定义 target 深度弱 |
| 29 | 测试 | partial | **214** 测；非像素 snapshot 主路径 |
| 30 | 模块结构 | partial | 目录齐；rpc/graphql/rtc/three 极简 |
| 31 | CLI | partial | start/run/dev/build/… 齐；doctor 等有 |
| 32 | Roadmap | done | CHANGELOG/tag 文档向 |
| 33 | Non-Goals | done | 文档有 |
| 34 | 不变量 | done(web) | validate_local + Playwright counter |
| 35 | 包元数据 | done | PyPI/GitHub 1.2.x（非 PLAN 字面 0.1.0） |

---

## 阶段文件 00–09

| 文档 | 状态 |
|------|:----:|
| 00_MASTER | partial — A 类 Web 核心真；gap-batch 扩 A 类子集 |
| 01_BOOTSTRAP | done |
| 02 v0.1 核心 | partial — Web 最小闭环有 |
| 03 v0.2 | partial |
| 04 v0.3 | partial |
| 05 v0.4 | partial |
| 06 v0.5–0.8 多端 | partial — 非 web 多为 JSON+壳；gui 已读 IR |
| 07 v0.9 | partial |
| 09 验收 | partial — 门禁绿 ≠ 能力闭环 |

---

## 最严重缺口（优先实现 · 已消化项已划掉）

1. ~~§13 `api.ws` / `api.sse` 缺失~~ → 工厂+handler 已验；真传输层仍待  
2. ~~§12 存储无文件后端~~ → FileBackend/configure_storage 已验  
3. ~~§4 Camera shake/zoom_to 缺陷~~ → 已验  
4. ~~§5 MotionChain `.then_`~~ → 已验  
5. ~~§18 canvas fluent~~ → 已验  
6. ~~§26 gui 不读 IR~~ → lowered.json + render_qt_tree 已验  
7. ~~§15 workers 非真线程~~ → ThreadPool 已验  
8. ~~§7 container queries~~ → CSS 输出已验  
9. ~~§20 平台静默 no-op~~ → 硬件/mobile 抛 UnsupportedCapability  
10. ~~§22 VirtualList 未接 emit~~ → virtual_list emit 已验  
11. ~~真 WS/SSE 传输~~ → aiohttp live mock 单测已验  
12. ~~媒体静默假返回 / FLIP 无 / rtc stub~~ → media honesty + 进程内 RTC + FLIP API  
13. ~~AABB 物理 / TMX CSV / IME / 文件 DnD~~ → 已验（**非**完整 Box2D / 完整 TMX）  
14. ~~drop_targets IR / forms async / router lazy / RTL·safe-area / pathfind+tile~~ → 已验  
15. ~~TMX base64/gzip · 嵌套 router layout~~ → 已验  
16. ~~TMX object layer · chunk 上传~~ → object 点/矩形/gid + upload_chunked 已验  
17. **仍缺**：真设备桥 / 浏览器 WebRTC / 完整 Box2D-class；多端原生深度；商店 C 类；完整 TMX（infinite/zstd/完整 polygon）；tus/断点续传；深嵌套 layout 组件树

---

## 本阶段 TODO（细粒度续接）

- [x] 写入诚实 08 矩阵（v6→…→**v12 object layers + chunked upload**）  
- [x] 实现 api.ws / api.sse + 单测  
- [x] 修 Camera.shake 衰减 / zoom_to / deadzone  
- [x] MotionChain 支持 PLAN 风格 `.then_.rotate()`  
- [x] canvas fluent Context API  
- [x] gui build 复用 desktop render_qt_tree  
- [x] workers ThreadPoolExecutor 真并行  
- [x] style container queries 输出  
- [x] storage 桌面文件后端（可选）  
- [x] platform 静默 pass → UnsupportedCapability + 测  
- [x] 更新 README 能力诚实矩阵  
- [x] media honesty + 进程内 RTC + FLIP + ws/sse 传输测  
- [x] AABB + 可选 pymunk + TMX CSV + IME + 文件 DnD  
- [x] drop_targets analyze_ui→lower→client_cfg；forms.validate_async；router lazy/layout；rtl/safe_area；astar_on_tilemap  
- [x] TMX base64/gzip/zlib；router group/parent/current_layouts  
- [x] TMX object layer 点/矩形/gid；upload_chunked + progress  
- [x] 回归 ruff/mypy/pytest/achecker（**214p**）  
- [x] `python -m build` + twine check（1.2.13）  
- [ ] 真设备桥 / 浏览器 WebRTC / 完整 Box2D-class / 多端原生深度  

---

## 已知降级 / 分级（A/B/C）

| 项 | 分级 | 说明 |
|----|:----:|------|
| Web compile-local | A | 真闭环 |
| Static SSG | A | 真 |
| Desktop .exe | A | 壳+PyInstaller 可选；**非完整原生 UI 树** |
| Android APK | A | Gradle 壳；SDK 可选 |
| iOS .ipa | B | 需 macOS CI；当前 web bundle 壳 |
| 商店签名上架 | C | 需账号 |
| 物理 / 图块 | A partial | 默认 AABB；可选 pymunk（非 box2d-py）；TMX 正交 CSV/base64(+gzip/zlib)+object 点/矩形/gid；A* 接 solid；无 infinite/zstd/完整 polygon |
| IME / 文件 DnD | A partial | Python 状态机 + Web composition / drop；**drop_targets IR 已贯通**；非桌面原生全路径 |
| 表单 async / 路由 nested / chunk 上传 | A partial | `validate_async` / lazy + group/parent/current_layouts；**upload_chunked 顺序 multipart**（非 tus）；深嵌套 layout 组件树仍浅 |
| RTL / safe-area | A partial | style 助手 → CSS；非完整双向布局引擎 |
| 浏览器 WebRTC / 真设备传感器 | A 待做 | RTC 仅进程内；硬件 API 显式 UnsupportedCapability |
| clipboard/notifications 宿主桥 | A 测桥 | **故意内存模拟**，文档已标明，非系统 API |
| media sim / RTC 进程内 | A 测桥 | 非 getUserMedia / 非 ICE |

---

## 审计日志

```
2026-07-25 全量重审：清空旧「终态」勾选；对照 PLAN+00–09；机器门禁 157p 仍绿
2026-07-25 审计结论：Web 反应式+编译真；多端/平台/媒体/ws 大量 interface-only
2026-07-25 gap-batch：ws/sse·camera·then_·canvas·workers·container·FileBackend·tasks·gui·PageStyle·easings·VirtualList emit；pytest 172p
2026-07-25 platform honesty：硬件/mobile 抛 UnsupportedCapability；宿主 clipboard 等保留；README 矩阵
2026-07-25 门禁全绿：ruff/mypy/achecker + pytest 177 passed, 1 skipped
2026-07-25 media/rtc/FLIP + ws/sse live：pytest 187p；build+twine 1.2.13；08 v8
2026-07-25 physics/tmx/IME/DnD：AABB+可选 pymunk+TMX CSV+composition+drop；pytest 196p；08 v9；不宣称 PLAN 字面闭环
2026-07-25 drop IR/forms async/router lazy/RTL/pathfind+tile：pytest 205p；08 v10；仍不宣称 PLAN 字面闭环
2026-07-25 TMX base64/gzip + nested router layouts：pytest 208p；08 v11；仍不宣称 PLAN 字面闭环
2026-07-25 TMX object layers + upload_chunked：pytest 214p；08 v12；仍不宣称 PLAN 字面闭环
```
