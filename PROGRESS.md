# EchoUI Progress

> **审计规则**：仅 `[x]` 表示本机命令验证通过；`[ ]` 未完成。

## 当前阶段

**v1.0.0 — 终态兑现**（2026-07-25）

---

## 09 协议 — 机器可检查项

| 项 | 状态 | 证据 |
|----|:----:|------|
| `pytest -q` | [x] | 106+ passed |
| `mypy echoui` | [x] | 84 files, no issues |
| `ruff check echoui tests` | [x] | All checks passed |
| `python achecker.py` | [x] | 全部合规 |
| `python -m build` + `twine check` | [x] | echoui-1.0.0 whl+sdist PASSED |
| `import echoui` | [x] | `1.0.0` |

---

## 09 协议 — CLI

| 命令 | 状态 |
|------|:----:|
| version / new / build (7 targets) / check / analyze / export / doctor / test / add | [x] |
| preview / dev | [x] |

---

## 架构终态（PLAN §34）

| 项 | 状态 |
|----|:----:|
| compile-local（actions + frame + validate） | [x] |
| router.navigate 本地 nav | [x] |
| 多屏 web/static | [x] |
| runtime 无 fetch / 无 /api/* | [x] |
| storage + webgpu + widgets runtime | [x] |
| SSR resumable hydrate | [x] |
| 八示例 web + static 全 build | [x] |

---

## 终态兑现清单

| 域 | 状态 | 证据 |
|----|:----:|------|
| Web 枚举 API（§4–§24 Web 子集） | [x] | 07_full_web + 08_media |
| 逃生层 §25 | [x] | 05_escape_layer |
| Chart.js / MapLibre | [x] | production 默认 |
| OPFS storage | [x] | storage.js |
| WebGPU free mode | [x] | gpu_backend=webgpu |
| 动画 §16 | [x] | test_animation |
| 平台 API §20 | [x] | test_platform_api |
| iOS CI 绕行 | [x] | `.github/workflows/ios-build.yml` |
| Android/Desktop build | [x] | test_desktop + build_target |

---

## 诚实边界（不可在本机伪造）

| 项 | 状态 | 说明 |
|----|:----:|------|
| PyPI 线上安装 | [ ] | 需有效 `PYPI_TOKEN`（403 待修） |
| iOS `.ipa` 签名 | [ ] | 需 macOS + 开发者账号 |
| 应用商店上架 | [ ] | 需用户资质 |

---

## 审计日志

```
2026-07-25 终态兑现：08_media、platform API 测、video/audio emit、README/CHANGELOG 1.0.0
2026-07-25 Web 完全兑现：07_full_web、runtime 扩展、101 pytest
2026-07-25 compile-local 终态 + achecker 全绿
```
