# AGENTS.md -- utils/ 目录易混淆点

> **活文档**：在此目录工作时更新本文件。
> 父级 AGENTS.md 已记录项目级陷阱，本文件仅记录 utils/ 特有的问题。

**最后更新：** 2026-05-16

---

## 易混淆之处

### [WARNING] validate_hex_color 在 color.py 和 validators.py 中重复
**混淆之处：** 同一函数存在于两个模块
**澄清：** validators.py 从 color.py 重新导入，功能完全相同
**正确做法：** 优先从 echoui.utils.color 导入，validators.py 仅用于验证器集合场景

### [WARNING] configure_platform() 必须在程序启动时调用
**混淆之处：** 以为这是一个可选工具函数
**澄清：** 在 Windows 上必须首先调用，设置 SelectorEventLoopPolicy
**正确做法：** 在 main() 或 __main__ 块的第一行调用 configure_platform()

### [WARNING] path_utils.get_project_root() 依赖固定目录深度
**混淆之处：** 以为通过智能检测找到项目根目录
**实际情况：** 使用 Path(__file__).resolve().parent.parent.parent.parent（固定 4 级）
**犯错后果：** 如果 path_utils.py 移动位置，返回错误路径
**正确做法：** 不要移动此文件位置

---

## 最近发现的意外日志

<!-- 追加新发现 -->
