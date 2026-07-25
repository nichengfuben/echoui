# EchoUI API 文档

用户向 API 文档入口。规范镜像见 [`docs-src/echoui/api/v0.1-index.md`](../../docs-src/echoui/api/v0.1-index.md)。

## 快速导航

| 文档 | 说明 |
|------|------|
| [sss.md](sss.md) | **SSS 范式**：Screen→Stage→Sprite 契约与示例 |
| [getting-started.md](getting-started.md) | 安装、Counter 示例、CLI |
| [plan-map.md](plan-map.md) | PLAN.md §0–§35 模块对照 |
| [targets.md](targets.md) | §26 渲染目标能力矩阵 |
| [non-goals.md](non-goals.md) | 明确非目标与 honest boundaries |
| [roles.md](roles.md) | 内建 role 与扩展方式 |

## PLAN 对齐摘要

完整规格见 [`.claude/docs/PLAN.md`](../../.claude/docs/PLAN.md)。

| § | 主题 | 状态 | 说明 |
|---|------|------|------|
| 0–1 | 纲领 / SSS | done | Screen→Stage→Sprite；flow/free |
| 2–3 | 架构 / 性能 | done | 本地编译 JS + Canvas2D/WebGPU + ~12KB runtime |
| 11–12 | 表单 / 存储 | done | forms + OPFS storage runtime |
| 22 | 数据展示 | done | Chart.js + MapLibre 生产级 |
| 9–10 | 反应式 / 事件 | done | build 时编译，运行时零 Python 往返 |
| 19 | 媒体/音频 | done | 08_media 示例 |
| 20 | 平台 API | done | test_platform_api |
| 25–27 | 逃生层 / 矩阵 / 编译 | done | raw/bridge + 八示例 build |
| 34 | 设计不变量 | done | validate_local_compile |

**诚实边界**：PyPI 上传需有效 token；iOS 签名与商店上架需外部资质。详见 [non-goals.md](non-goals.md)。

## 版本

当前发布线：**1.0.0**（PyPI：https://pypi.org/project/echoui/）
