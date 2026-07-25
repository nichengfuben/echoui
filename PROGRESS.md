# EchoUI Progress

> **审计规则**：仅 `[x]` 表示本机命令验证通过；`[ ]` 未完成。  
> **唯一真相来源**：本文件 + `08_全量追踪矩阵.md`。

## 当前阶段

**v1.2.8 — Web 终态 + CI 发布闭环**（2026-07-25）

PyPI **1.2.8**；GitHub **Publish workflow** + `PYPI_API_TOKEN` 已同步。

---

## 09 协议 — 机器可检查项

| 项 | 状态 | 证据 |
|----|:----:|------|
| `pip install echoui` | [x] | PyPI 1.2.8 |
| `pytest -q` | [x] | 128 passed |
| `mypy echoui` | [x] | 84 files |
| `ruff check echoui tests` | [x] | 全绿 |
| `python achecker.py` | [x] | 全绿 |
| `python -m build` + `twine check` | [x] | 1.2.8 PASSED |
| tag push → PyPI CI | [x] | publish.yml + PYPI_API_TOKEN |
| `echoui new` + `build --target web` | [x] | pip workflow 测 |
| 九示例 web+static build | [x] | test_build_all_examples |
| `echoui dev` 热重建无循环 | [x] | dist/ 忽略 + 1.2.6 |
| `file_input` → Signal 传图 | [x] | 1.2.5 factory 修复 |
| `echoui build --target tui` IR 渲染 | [x] | compose_ir + test_build_tui |
| Desktop `.exe` 本机验证 | [ ] | PyInstaller 未验 |
| Android `.apk` 本机验证 | [ ] | 未验 |
| iOS CI artifact 绿 | [ ] | workflow 存在，未确认跑通 |
| 08 矩阵全 done | [ ] | Web A 类 done；native 仍 partial |

---

## Web compile-local 终态（§34）

| 域 | 状态 | 证据 |
|----|:----:|------|
| compile-local 架构 + validate_local | [x] | build 硬失败未编译 handler |
| SSS Web 编译 + free GPU | [x] | 跑酷贴图/色块分离 |
| 反应式 Signal/Store + image src 绑定 | [x] | test_web_reactive, test_media_features |
| 路由静态多屏 | [x] | 04 示例 + nav 编译 |
| 逃生层 raw.js | [x] | 05_escape_layer |
| 50+ role Web emit | [x] | emit_roles + test_all_roles_emit |
| file_input 上传 + wireFiles | [x] | ui.js FileReader → Signal |
| overlay modal/drawer | [x] | wireOverlays |
| audio.play compile-local | [x] | audio.js + 跑酷跳跃音 |
| 表单 file 校验 | [x] | file_size/type/max_files |
| VirtualList / DataTable | [x] | echoui.data + 单测 |
| i18n plural / format | [x] | test_data_i18n_forms |
| collab SyncRelay | [x] | test_collab_sync |
| gestures + 虚拟列表滚动 | [x] | gestures.js |
| Chart.js / MapLibre | [x] | 07_full_web |
| CLI dev/build/new | [x] | dev watch 过滤 dist |

---

## 未完成 — 诚实边界

### P2 — 多端 native

- [ ] Desktop：PyInstaller `.exe` 本机验
- [ ] Android：Gradle APK 本机验
- [ ] iOS：Actions artifact 下载验证

### P3 — 生态

- [x] docs-src 核心 API 图鉴（9 条：media/stage/ecosystem）
- [ ] docs-src 50+ role 全量四件套
- [ ] Playwright escape+signal 集成测
- [ ] pycrdt 网络协作（当前 LWW SyncRelay）

---

## 审计日志

```
2026-07-25 v1.2.8 CI publish + docs 图鉴 + PyPi token 全仓同步
2026-07-25 v1.2.7 Web compile-local 终态：127 pytest；file_input/dev watch/跑酷造型；PyPI+GH
2026-07-25 v1.2.6 dev watch 忽略 dist 修复重建循环
2026-07-25 v1.2.5 file_input 工厂覆盖修复 + 跑酷造型切换
2026-07-25 诚实复审计：撤回过度终态宣称；08 矩阵 v2
```
