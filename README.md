# EchoUI — Universal Python-first UI framework

One **Screen–Stage–Sprite** paradigm compiles to Web, desktop, mobile, TUI, and GUI.

**Version:** 1.2.13 · **License:** MIT · **PyPI:** `pip install echoui` · **GitHub:** [nichengfuben/echoui](https://github.com/nichengfuben/echoui)

> **诚实说明**：包可安装、机器门禁可绿，**不等于** PLAN 字面全能力闭环。请以下方能力矩阵为准。

## 像 npm 一样用

| npm | EchoUI |
|-----|--------|
| `npm install` | `pip install echoui[web]` |
| `npm start` | `echoui start` |
| `npm run build` | `echoui run build` 或 `echoui build --target web` |
| `npm run dev` | `echoui dev` / `echoui run dev` |

```bash
pip install echoui[web]
echoui new my-app
cd my-app
pip install -e .
echoui start
```

脚本定义在 `pyproject.toml` 的 `[tool.echoui.scripts]`（同 npm 的 `package.json` scripts）：

```toml
[tool.echoui.scripts]
start = "dev --port 8765"
build = "build --target web"
```

PyPI 尚未发布目标版本时，可从 GitHub 安装：

```bash
pip install "echoui[web] @ git+https://github.com/nichengfuben/echoui.git"
```

## Quick Start（已有 main.py）

```python
from echoui import App, Screen, Store, col, text, button

class CounterStore(Store):
    count: int = 0

store = CounterStore()

class Counter(Screen):
    def build(self):
        return col(
            text(lambda: f"Count: {store.count}"),
            button("+1", on_click=lambda: setattr(store, "count", store.count + 1)),
        )

app = App(screens=[Counter], initial="Counter")
```

```bash
echoui build --target web
echoui dev --port 8765
```

## 能力矩阵（诚实）

| 领域 | 状态 | 说明 |
|------|:----:|------|
| 反应式 Signal/Store/computed | **done** | 细粒度更新，无 VDOM |
| Web 编译 (DOM + runtime JS) | **done** | `echoui build --target web` |
| Static SSG | **done** | 预渲染 HTML |
| 路由 / 表单校验 / REST+query | partial | lazy loader + `group`/`parent`/`current_layouts` + `validate_async` 已验；**`upload_chunked` + progress 已验**；深嵌套 layout 语义仍浅 |
| `api.ws` / `api.sse` 客户端 | partial | **aiohttp 真传输**（单测 live mock）；无 aiohttp 时降级 |
| 存储 local/session | partial | 默认可切 FileBackend；sqlite 真 |
| 动画 tween/spring + FLIP | partial | 具名 easing + `flip`/`capture_rects`；列表 emit 接线有限 |
| Camera / MotionChain `.then_` | partial | shake/zoom/deadzone / 属性链已接 |
| Canvas fluent / VirtualList emit | partial | web 窗口化接线有限 |
| workers 线程池 | partial | ThreadPoolExecutor；wasm 仍弱 |
| GUI / desktop / TUI / mobile 目标 | interface-only～partial | 产物壳或 Qt 子集；非完整原生树 |
| iOS 真机 `.ipa` | B 类 | 需 macOS/CI；仓库为 web bundle 壳 |
| 平台 clipboard/notifications | partial | **宿主内存桥**（测/演示）；非系统 API |
| 生物识别/蓝牙/NFC 等 | interface-only | 无桥时 **`UnsupportedCapability`**，不静默成功 |
| 媒体 camera/geo/sensors | partial | 无桥抛 `UnsupportedCapability`；`enable_media_sim` 内存桩 |
| RTC DataChannel | partial | **进程内** peer 投递；非浏览器 WebRTC |
| 物理 AABB / 可选 pymunk | partial | 默认 AABB；`create_world("pymunk")` 需 `echoui[physics]`；**非**完整 Box2D |
| TMX 图块 | partial | `load_tmx` 正交 CSV/base64（+gzip/zlib）+ object layer 点/矩形/gid 子集；无 infinite / zstd / 完整 polygon 顶点 |
| IME composition / 文件 DnD | partial | Python API + Web composition*/drop；**drop_targets IR→client_cfg 已贯通**；非桌面原生全路径 |
| RTL / safe-area 样式 | partial | `rtl`/`ltr`/`safe_area`/`writing_mode` → CSS；非完整双向布局引擎 |
| pathfind + tile solid | partial | `astar_on_tilemap` / `passable_from_tilemap` |
| 真设备桥 / 浏览器 WebRTC | stub / 待做 | 硬件原生与 ICE 仍弱 |

图例：`done` = 可依赖的 A 类实现 · `partial` = 子集真 · `interface-only` = 可 import 但勿当生产完成。

## CLI

| Command | Description |
|---------|-------------|
| `echoui new [name]` | 脚手架（main.py + pyproject.toml） |
| `echoui start` | 启动开发服务器（同 `npm start`，默认 8765） |
| `echoui run <script>` | 运行 pyproject 脚本（同 `npm run`） |
| `echoui dev` | 开发服务器（watch + 静态服务） |
| `echoui build --target web\|static\|tui\|desktop\|gui\|android\|ios` | 编译 |
| `echoui preview` | 预览已 build 的 dist |
| `echoui check` | 校验项目 |
| `echoui version` | 版本 |

## 示例

`examples/` 含 hello、counter、跑酷 `06_runner`、全功能 dashboard `07_full_web` 等。

## License

MIT — see [LICENSE](LICENSE).
