from __future__ import annotations

"""高度自定义化验证脚本 - 验证 EchoUI 的自定义主题、组件组合、嵌套布局、扩展能力。"""

import sys

if sys.platform == "win32":
    from echoui.utils.compat import configure_platform
    configure_platform()


def verify_custom_theme() -> bool:
    """验证自定义主题注册与使用。"""
    from dataclasses import replace

    from echoui.core.theme import Theme, ThemeConfig
    from echoui.components.notification import Notification

    print("=" * 60)
    print("场景 1: 自定义主题注册与使用")
    print("=" * 60)

    # 1. 注册自定义主题
    custom = ThemeConfig(
        name="my_custom_theme",
        primary_start="#FF00FF",
        primary_end="#00FFFF",
        border_start="#FF6600",
        border_end="#0066FF",
        accent_start="#FFFF00",
        accent_end="#FF0066",
        success="#00FF00",
        warning="#FFAA00",
        error="#FF0000",
        info="#00AAFF",
        muted="#888888",
        bg_dark="#0A0A0A",
        bg_light="#1A1A1A",
        text_primary="#FFFFFF",
        text_secondary="#AAAAAA",
    )
    Theme.register(custom)

    # 2. 验证注册成功
    names = Theme.list_names()
    assert "my_custom_theme" in names, f"自定义主题未注册: {names}"
    print(f"  [PASS] 自定义主题注册成功，当前主题数: {len(names)}")

    # 3. 使用自定义主题创建组件
    got = Theme.get("my_custom_theme")
    assert got.primary_start == "#FF00FF"
    assert got.border_end == "#0066FF"
    print(f"  [PASS] Theme.get('my_custom_theme') 颜色正确")

    # 4. 用自定义主题创建组件
    n = Notification(theme=got, normal_mode=True)
    out = n.success("自定义主题测试").render()
    assert "[OK]" in out
    print(f"  [PASS] 使用自定义主题创建 Notification: {out}")

    # 5. 基于已有主题创建变体（replace 模式）
    ocean = Theme.get("ocean")
    variant = replace(ocean, name="ocean_dark", bg_dark="#000000")
    Theme.register(variant)
    assert Theme.get("ocean_dark").bg_dark == "#000000"
    print(f"  [PASS] 基于 replace 创建主题变体")

    print()
    return True


def verify_component_composition() -> bool:
    """验证组件自由组合：Box 套 Table、Table 套 Box 内容等。"""
    from echoui.components.box_builder import BoxBuilder
    from echoui.components.table_builder import TableBuilder
    from echoui.components.key_value_list import KeyValueList
    from echoui.components.tree_view import TreeView
    from echoui.components.ascii_art_builder import AsciiArtBuilder
    from echoui.components.panel_builder import PanelBuilder

    print("=" * 60)
    print("场景 2: 组件自由组合与嵌套")
    print("=" * 60)

    # 1. Box 套 Table：把表格放进盒子
    table = (
        TableBuilder(normal_mode=True)
        .set_headers(["模块", "状态"])
        .add_row(["core", "OK"])
        .add_row(["components", "OK"])
        .render()
    )
    boxed_table = BoxBuilder(normal_mode=True).content(table).title("模块状态").build()
    assert "模块状态" in boxed_table
    assert "core" in boxed_table
    assert "components" in boxed_table
    print(f"  [PASS] Box 套 Table 嵌套渲染成功")
    for line in boxed_table.split("\n")[:5]:
        print(f"         {line}")
    print("         ...")

    # 2. KeyValueList 链式添加
    kvl = KeyValueList()
    result = (
        kvl.add("框架", "EchoUI")
        .add("版本", "2.0.0")
        .add("语言", "Python")
        .add("平台", "跨平台")
        .render()
    )
    assert "框架" in result and "EchoUI" in result
    assert "版本" in result and "2.0.0" in result
    # 验证冒号对齐
    lines = result.split("\n")
    colons = [line.index(":") for line in lines if ":" in line]
    assert len(set(colons)) == 1, f"冒号未对齐: {colons}"
    print(f"  [PASS] KeyValueList 链式添加 + 冒号对齐")
    for line in lines:
        print(f"         {line}")

    # 3. TreeView 嵌套数据
    tree_data = {
        "src": {
            "core": {
                "exceptions.py": "异常定义",
                "renderer.py": "渐变渲染",
                "theme.py": "主题系统",
            },
            "components": {
                "base_component.py": "抽象基类",
                "console_ui.py": "主控制器",
            },
        },
        "tests": {
            "unit": "单元测试",
            "integration": "集成测试",
        },
    }
    tree = TreeView(data=tree_data, normal_mode=True)
    tree_out = tree.render()
    assert "core" in tree_out
    assert "renderer.py: 渐变渲染" in tree_out
    assert "unit: 单元测试" in tree_out
    print(f"  [PASS] TreeView 嵌套字典渲染")
    for line in tree_out.split("\n")[:6]:
        print(f"         {line}")
    print("         ...")

    # 4. AsciiArtBuilder 自定义艺术字
    art = (
        AsciiArtBuilder()
        .add_line("  ____ ___  ____ ")
        .add_line(" / ___/ _ \\/ ___|")
        .add_line("| |  | | | \\___ \\")
        .add_line("| |__| |_| |___) |")
        .add_line(" \\____\\___/|____/ ")
        .build()
    )
    assert "____" in art
    lines = art.split("\n")
    assert len(lines) == 5
    print(f"  [PASS] AsciiArtBuilder 自定义艺术字 ({len(lines)} 行)")

    # 5. PanelBuilder 自定义面板
    panel = PanelBuilder()
    panel_out = panel.title("系统信息").content("CPU: 8核\n内存: 16GB\n磁盘: 512GB").render()
    assert "系统信息" in panel_out
    assert "CPU: 8核" in panel_out
    print(f"  [PASS] PanelBuilder 自定义面板")
    for line in panel_out.split("\n"):
        print(f"         {line}")

    print()
    return True


def verify_column_layout() -> bool:
    """验证列布局：多列并排、高度对齐。"""
    from echoui.components.column_layout import ColumnLayout

    print("=" * 60)
    print("场景 3: 列布局自定义")
    print("=" * 60)

    # 1. 基础两列
    col1 = "名称: EchoUI\n版本: 2.0.0\n语言: Python"
    col2 = "核心: 12模块\n组件: 20个\n测试: 355个"
    layout = ColumnLayout([col1, col2])
    out = layout.render()
    lines = out.split("\n")
    assert len(lines) == 3, f"行数不匹配: {len(lines)}"
    assert "EchoUI" in lines[0] and "12模块" in lines[0]
    print(f"  [PASS] 两列并排渲染 ({len(lines)} 行)")
    for line in lines:
        print(f"         {line}")

    # 2. 三列（高度不一致，自动对齐）
    col_a = "A1\nA2\nA3"
    col_b = "B1"
    col_c = "C1\nC2"
    layout3 = ColumnLayout([col_a, col_b, col_c])
    out3 = layout3.render()
    lines3 = out3.split("\n")
    assert len(lines3) == 3, f"三列行数不匹配: {len(lines3)}"
    assert "A1" in lines3[0] and "B1" in lines3[0] and "C1" in lines3[0]
    print(f"  [PASS] 三列不等高自动对齐")
    for line in lines3:
        print(f"         {line}")

    print()
    return True


def verify_component_extensibility() -> bool:
    """验证组件可扩展性：继承 BaseComponent 创建自定义组件。"""
    from typing import TYPE_CHECKING, Optional

    from echoui.components.base_component import BaseComponent
    from echoui.core.renderer import GradientRenderer
    from echoui.core.theme import ThemeConfig

    print("=" * 60)
    print("场景 4: 组件可扩展性（继承 BaseComponent）")
    print("=" * 60)

    # 创建一个自定义组件
    class StatusBadge(BaseComponent):
        """自定义状态徽章组件。"""

        def __init__(
            self,
            label: str = "",
            status: str = "info",
            renderer: Optional[GradientRenderer] = None,
            normal_mode: bool = False,
            theme: Optional[ThemeConfig] = None,
        ) -> None:
            super().__init__(renderer=renderer, normal_mode=normal_mode, theme=theme)
            self._label = label
            self._status = status

        def label(self, text: str) -> "StatusBadge":
            self._label = text
            return self

        def status(self, s: str) -> "StatusBadge":
            self._status = s
            return self

        def render(self) -> str:
            prefix = {
                "success": "[OK]",
                "warning": "[!]",
                "error": "[X]",
                "info": "[i]",
            }.get(self._status, "[?]")
            if self._normal_mode:
                return f"{prefix} {self._label}"
            return f"{prefix} {self._label}"

    badge = StatusBadge(normal_mode=True)
    out = badge.label("部署成功").status("success").render()
    assert "[OK]" in out and "部署成功" in out
    print(f"  [PASS] 自定义 StatusBadge 组件: {out}")

    # 链式调用验证
    badge2 = StatusBadge(normal_mode=True)
    out2 = (
        badge2
        .label("编译中")
        .status("info")
        .render()
    )
    assert "[i]" in out2
    print(f"  [PASS] 自定义组件链式调用: {out2}")

    # 多实例独立状态
    b1 = StatusBadge(normal_mode=True).label("模块A").status("success")
    b2 = StatusBadge(normal_mode=True).label("模块B").status("error")
    assert b1.render() != b2.render()
    print(f"  [PASS] 多实例独立状态: '{b1.render()}' vs '{b2.render()}'")

    print()
    return True


def verify_chained_workflow() -> bool:
    """验证复杂链式工作流：ConsoleUI 组合多种输出。"""
    import io

    from echoui.components.console_ui import ConsoleUI
    from echoui.components.notification import Notification
    from echoui.components.box_builder import BoxBuilder

    print("=" * 60)
    print("场景 5: 复杂链式工作流")
    print("=" * 60)

    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured

    try:
        ui = ConsoleUI(normal_mode=True)
        ui._output_stream = captured

        # 模拟真实工作流：初始化 -> 检查 -> 报告 -> 总结
        (
            ui.print("EchoUI 构建系统")
            .rule("=", 40)
            .info("开始构建...")
            .success("核心引擎编译完成")
            .success("组件库构建完成")
            .success("测试套件通过")
            .warning("覆盖率 97%（目标 90%）")
            .newline()
        )

        # 用 BoxBuilder 构建摘要框
        summary = (
            BoxBuilder(normal_mode=True)
            .content("测试: 355 passed\n覆盖率: 97%\nmypy: 0 errors")
            .title("构建报告")
            .build()
        )
        ui.print(summary)

        ui.rule("=", 40)
        ui.success("构建成功!")

        output = captured.getvalue()
    finally:
        sys.stdout = old_stdout

    assert "EchoUI 构建系统" in output
    assert "[OK]" in output
    assert "[i]" in output
    assert "构建报告" in output
    assert "355 passed" in output
    assert "构建成功" in output
    line_count = len(output.strip().split("\n"))
    print(f"  [PASS] 复杂链式工作流: {line_count} 行输出")
    print("  输出预览:")
    for line in output.strip().split("\n")[:15]:
        print(f"    {line}")
    print("    ...")

    print()
    return True


def verify_design_token_customization() -> bool:
    """验证设计令牌自定义：间距、排版、圆角、阴影的组合使用。"""
    from echoui.core.layout import resolve_breakpoint
    from echoui.core.typography import TYPE_SCALE_MAP
    from echoui.core.spacing import SPACING_MAP
    from echoui.core.design_tokens import RADIUS_MAP, SHADOW_MAP

    print("=" * 60)
    print("场景 6: 设计令牌自定义组合")
    print("=" * 60)

    # 1. 自定义视口计算
    bp_320 = resolve_breakpoint(320)
    bp_1920 = resolve_breakpoint(1920)
    bp_4000 = resolve_breakpoint(4000)
    assert bp_320.layout_mode == "single"
    assert bp_1920.layout_mode == "triple"
    assert bp_4000.layout_mode == "multi"
    print(f"  [PASS] 320px=single, 1920px=triple, 4000px=multi")

    # 2. 排版 scale 自定义使用（compute_px 是实例方法）
    h1 = TYPE_SCALE_MAP["h1"].compute_px(1920)  # base 16px
    body = TYPE_SCALE_MAP["body"].compute_px(1024)
    small = TYPE_SCALE_MAP["small"].compute_px(320)
    assert h1 > body > small
    print(f"  [PASS] 排版: h1(1920px)={h1:.1f}px > body(1024px)={body:.1f}px > small(320px)={small:.1f}px")

    # 3. 间距 scale 使用（compute_px 是实例方法）
    s_1 = SPACING_MAP["3xs"].compute_px(320)
    s_4 = SPACING_MAP["sm"].compute_px(1024)
    s_8 = SPACING_MAP["3xl"].compute_px(1920)
    assert s_1 < s_4 < s_8
    print(f"  [PASS] 间距: 3xs(320px)={s_1:.1f}px < sm(1024px)={s_4:.1f}px < 3xl(1920px)={s_8:.1f}px")

    # 4. 圆角/阴影令牌使用
    assert len(RADIUS_MAP) == 7
    assert len(SHADOW_MAP) == 5
    print(f"  [PASS] 圆角 7 级, 阴影 5 级均可用")

    print()
    return True


def main() -> None:
    """运行所有自定义化验证。"""
    results: dict[str, bool] = {}

    scenarios = [
        ("自定义主题", verify_custom_theme),
        ("组件组合", verify_component_composition),
        ("列布局", verify_column_layout),
        ("组件扩展", verify_component_extensibility),
        ("链式工作流", verify_chained_workflow),
        ("设计令牌", verify_design_token_customization),
    ]

    for name, fn in scenarios:
        try:
            results[name] = fn()
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False

    print("=" * 60)
    print("高度自定义化验证总结")
    print("=" * 60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    for name, ok in results.items():
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")
    print(f"\n总计: {passed}/{total} 通过")

    if passed < total:
        sys.exit(1)
    else:
        print("\n所有自定义化验证通过!")


if __name__ == "__main__":
    main()
