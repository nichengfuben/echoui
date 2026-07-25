# Changelog

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
