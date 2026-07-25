# Changelog

## 1.2.11 — Sprite 全量运动/感知 + 持久化 + 响应式 (2026-07-25)

- **Sprite**：`point_toward` / `bounce_on_edge` / `flip_*` / `orbit` / `say` / `split_to` / `image()` 等
- **MotionChain**：`when().otherwise()` 条件分支修复
- **Store 持久化**：`persist_mixin("local")` + `_load_persisted()`
- **布局**：`row/col/grid(responsive={...})` → emit 媒体查询 CSS
- **style**：hover/dark/media 嵌套规则编译
- **files.pick**：桌面 tkinter 原生选文件 → data URL

## 1.2.10 — 造型 API (2026-07-25)

- **`costume()` / `bind_costumes()`**：命名造型 + `switch["name"]` / `next_costume` / `save_costume`（compile-local）
- **`Sprite`**：`costumes`、`costume_src`、`switch_costume(name|idx)`、`next_costume()`
- 跑酷示例移除造型 UI；演示在 `examples/08_media`
- 编译器：`__echoui_source__` + 仅 `<` 比较的可编译 handler 生成

## 1.2.9 — 终态 (2026-07-25)

- **Desktop**：`test_build_desktop` + Windows PyInstaller `.exe` 冒烟
- **Android**：Gradle 工程生成 + `ANDROID_SDK_ROOT` 时 `assembleDebug` APK
- **iOS**：`test_build_ios` + CI `ios-build.yml` web bundle artifact
- **Playwright**：counter 点击 + escape 层加载集成测
- **collab**：`echoui[collab]` pycrdt `PyCRDTSession` + merge_updates
- **docs**：82 role 全量图鉴 `role-catalog.md`（`scripts/gen_role_docs.py`）
- **CLI**：`echoui build --target android --package` → APK（需 SDK）

## 1.2.8 — CI PyPI 自动化 + 文档图鉴扩展 (2026-07-25)

- **GitHub Actions**：`publish.yml` — tag `v*` 自动 twine 发布（`PYPI_API_TOKEN`）
- **docs-src**：媒体上传、Stage/overlay、forms/data/i18n 图鉴条目（9 条 API 索引）
- **PyPi 生态**：`X:\Project\PyPi\scripts\sync_pypi_token.ps1` 统一同步各 SDK `.env` 与 GH secret

## 1.2.7 — Web compile-local 终态 (2026-07-25)

- **终态范围**：compile-local Web 栈闭环（§34）；127 pytest + ruff + mypy + achecker 全绿
- **跑酷**：compile-local handler（无 lambda）；双槽位造型保存/切换（C 键）
- **质量**：ruff/mypy 清理；TUI ProgressBar API 对齐；ui_collect 返回类型修正
- **测试**：conftest 禁用 localhost 代理，修复集成测 502 flake
- **文档**：PROGRESS / 08 矩阵更新为诚实 Web 终态

## 1.2.6 — dev watch 重建循环修复 (2026-07-25)

- `echoui dev` watch 忽略 `dist/`、`build/`、`.echoui/`，避免 compile→write→rebuild 死循环

## 1.2.5 — file_input 上传接线修复 (2026-07-25)

- 专用 `file_input` 不再被 `_BUILTIN_ROLES` 工厂覆盖；`file_inputs` 正确写入 client cfg
- 跑酷示例：保存/切换造型（双槽位 compile-local）

## 1.2.4 — runtime 打包修复（替换损坏的 1.2.3 wheel）(2026-07-25)

- **1.2.3 PyPI wheel 损坏**（仅含 JS、无 Python 模块），本版为完整 wheel
- `load_web_runtime` 使用 `importlib.resources`，安装后 `echoui dev` 可正常 Rebuild

## 1.2.3 — runtime/web 打包修复 (2026-07-25) [YANK — 损坏 wheel]

- **wheel/sdist**：`hatch` `force-include` 强制打入 `echoui/runtime/web/*.js`
- **`load_web_runtime`**：`importlib.resources` + 源树双路径，缺失时给出 reinstall 提示
- 修复 PyPI 安装后 `echoui dev` Rebuild 找不到 `core.js`

## 1.2.2 — 跑酷 GPU 颜色修复 (2026-07-25)

- **free-mode GPU**：`image`/控件不再批渲染为 `#888` 灰块，仅 `box`+`background` 进 canvas
- **Stage 文字**：`.e-stage-inner .e-text` 白字+阴影，分数可读
- 新增 `tests/unit/test_free_gpu.py`

## 1.2.1 — 全量 role emit / TUI IR / 数据与协作 (2026-07-25)

- **`emit_roles`**：50+ 内建 role 统一 HTML emit（virtual_list、stepper、radio_group 等）
- **TUI**：IR 驱动 Textual compose（`compose_ir`），JSON 导出脱敏
- **Desktop**：扩展 input/checkbox/progress 等 Qt 渲染
- **`echoui.data`**：VirtualList / DataTable
- **`echoui.collab`**：SyncRelay / SyncClient WebSocket 同步
- **forms**：file_size / file_type / max_files 校验器
- **i18n**：plural / format_number / format_currency
- **runtime**：gestures.js（pointer 拖拽 + 虚拟列表滚动）+ upload 进度
- **examples/09_full**：全 role 展示示例

## 1.2.0 — 媒体/上传/音频实装 (2026-07-25)

- **`echoui.audio`**：`play` / `play_bgm` / `set_volume` / `TTS` + Web runtime `audio.js`
- **`file_input`**：Web `type=file` emit + FileReader → Signal 绑定
- **`image(src=signal)`**：响应式 `src` 属性绑定
- **overlay**：modal/drawer/sheet Web 渲染 + open signal
- **platform/media/storage.files/desktop/mobile/rtc/graphql/rpc/three**：实装 API（非空壳）
- **跑酷示例**：上传背景/角色图 + 跳跃音效
- runtime 扩展：`platform.js` + `ui.js`（~16KB bundle）

## 1.0.1 — physics extra 兼容 Python 3.14 (2026-07-25)

- **`physics` extra**：`box2d-py` 替换为 `pymunk>=7.0.0`（PyPI 有 3.14 wheel，持续维护）
- `pip install echoui[all]` 在 Python 3.14 上可完整安装
- 内置 AABB 物理（`echoui.physics.World`）不变，不依赖可选 extra

## 1.0.0 — 终态兑现 (2026-07-25)

- **Web 完全兑现**：Chart.js / MapLibre 生产级、OPFS storage、WebGPU、SSR resume 水合
- **Runtime 扩展**：`storage.js` + `webgpu.js` + `widgets.js` 并入 `runtime.js`（~12KB）
- **八示例** web+static 全 build（含 `07_full_web` dashboard、`08_media` 音视频）
- **101+ pytest** + achecker 全绿；§34 compile-local 不变量硬校验
- iOS CI workflow（`ios-build.yml`）+ 诚实边界文档（PyPI / 商店签名）

## 1.0.0 — Compile-local 终态 (PLAN §34)

- **架构终态**：所有 UI 事件/帧循环在 `echoui build` 时编译为本地 JS；客户端零 Python、零 `/api/*` 往返
- `emit_actions` 复用 `emit_frame` AST→JS 管线；`validate_local_compile` build 硬失败
- `router.navigate('/path')` 编译为 `{k:"nav", href:"…html"}`；多屏 app 合并 handler 校验
- Web/Static 多屏输出 `index.html` + `{screen}.html` + `screens.json`
- `core.js` 纯本地 Signal + runA + localF + nav；dev = watchfiles + 静态服务
- 六示例 web+static 全 build；collab/i18n/overlay/router/cli 补测
- `docs/api` 合并为 7 文件（achecker 合规）

## 0.9.4

- Fix Web SSR: inject GPU canvas + dimensions for free-mode stage children (runner game visible)
- Fix `frame_script` spawn loop: obstacles now spawn at x=660 in static/local frame mode
- GPU runtime fallback: if canvas missing, unhide DOM sprites instead of blank stage
- **SSS alignment (PLAN §1/§4):** game screens use `layout="free"` and `build() → stage(...)`; HUD/buttons are Sprites inside Stage, not `col()` wrapping stage; web emit collapses free Screen→Stage to single stage surface
- Examples `03_game_free_mode`, `04_multi_screen_game`, `06_runner` updated to SSS tree
- Tests: 66 passed; SSS tree assertion + GPU canvas/spawn checks

## 0.9.3

- Web reactive runtime: Signal store, text/style bindings, local actions, `/api/action` + `/api/frame` without full reload
- `@on("frame")` / `@on("keydown", key=...)` wired through compiler keymap and dev server dispatch
- DOM event delegation: click, dblclick, hover, focus/blur, wheel, contextmenu, drag (compiler + `core.js`)
- Static builds: client-side `frame_script` local rAF loop (no server); ships `runtime.js`
- GPU free-mode: Canvas2D batched rendering for `stage layout=free` sprites
- Advanced roles: chart (bar canvas), map (placeholder), gantt (timeline bars) web emit
- Desktop target: Qt widget tree from lowered IR; Android/iOS webview asset bundles
- Sprite motion/sensing, MotionChain, Stage/Camera, frame testing via `tick()`
- Example `06_runner` — 2D endless runner on Store + stage free mode

## 0.9.2

- Align public API with PLAN.md §6: export 50+ built-in role factories from `echoui`
- PLAN §28 plugin decorators: `Plugin`, `compiler_pass`, `role`, `target`, `api_binding`
- PLAN §31 CLI: `preview`, `export`, `analyze`, `test`, `doctor`, `add`; build targets `android`/`ios`
- PLAN §29: `echoui.testing.a11y_audit` with `.passes`
- `docs/api/plan-map.md` — PLAN §0–§35 → module index
- PLAN §15：`async_`/`workers`/`wasm`/`tasks` API 落点
- PLAN §17：`clone_pool` 对象池
- `docs/api/plan-alignment.md` — PLAN 各节对齐摘要

## 0.9.1

- Fix TUI build JSON serialization for reactive lambdas
- Add `python -m echoui` entry via `__main__.py`
- Bootstrap modules, examples `01_hello_web` / `03_game_free_mode`, visual/a11y tests
- docs-src API catalog entries; iOS CI workflow; reactive benchmark script

## 0.9.0

- Release-ready packaging: version aligned across pyproject, package, docs, and CHANGELOG
- Quality gate: ruff, mypy, pytest; wheel build + twine check
- Marks v0.1–v0.9 feature set as the first public-ready cut (see PROGRESS.md)

## 0.1.0

- Reactive core: Signal, Computed, Effect, batch, Store
- Screen–Stage–Sprite paradigm with flow and free layout
- Web compiler pipeline: parser → analyzer → optimizer → lower → emit → bundler
- CLI: new, dev, build, check, version
- Testing harness: mount, fire, tick, snapshot
- Router with guards and middleware
- Forms, storage, query, animation, gestures, overlay
- Escape layer (raw.js/html/css) and bridge.web_api
- Static, TUI, desktop, GUI, Android template targets
- Collab CRDT, data tables, i18n, a11y, print, platform, plugins
