# 渲染目标能力矩阵（PLAN §26）

| 能力 | web | static | tui | desktop | gui | android | ios |
|------|:---:|:------:|:---:|:-------:|:---:|:-------:|:---:|
| Screen / Stage / Sprite | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| flow 布局 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| free 布局 | ✓ | ✓ | 降级 | ✓ | ✓ | ✓ | ✓ |
| 反应式 Store | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 路由 | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| HTTP 客户端 | ✓ | — | — | ✓ | ✓ | ✓ | ✓ |
| 表单校验 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| SSR / resumable | ✓ | — | — | — | — | — | — |
| 逃生层 raw.js/html | ✓ | ✓ | — | — | — | — | — |
| PWA / offline | ✓ | — | — | — | — | — | — |
| PySide6 窗口 | — | — | — | ✓ | ✓ | — | — |
| WebView 壳 | — | — | — | ✓ | — | ✓ | ✓ |
| 打包 .exe / .apk / .ipa | — | — | — | A* | — | A* | B** |

\* A 类：需本机工具链（PySide6+PyInstaller / Android SDK）。  
\** B 类：iOS 需 macOS CI（`.github/workflows/ios-build.yml`）。

## 角色降级（节选）

| role | web | tui | desktop/gui |
|------|-----|-----|-------------|
| text / button / input | 原生 | styled cells | Qt 控件 |
| canvas / chart | canvas/svg | braille 近似 | QPainter |
| map / viewport3d | embed/WebGL | placeholder | native GL 或 escape |
| video / audio | HTML5 | stub | QMediaPlayer |

完整 role 列表见 PLAN §6；工厂函数均从 `echoui` 包导出。不支持时抛 `UnsupportedCapability` 或文档标注降级。

## 构建命令

```bash
echoui build --target web|static|tui|desktop|gui|android|ios
```

见 [getting-started.md](getting-started.md) 与 [plan-map.md](plan-map.md)。
