from __future__ import annotations

"""真实场景验证脚本 - 验证 EchoUI 在实际终端中的渲染与交互。"""

import asyncio
import sys

# Windows 兼容
if sys.platform == "win32":
    from echoui.utils.compat import configure_platform
    configure_platform()


def verify_basic_rendering() -> bool:
    """验证基础渲染：通知、进度条、表格、盒子。"""
    from echoui.components.notification import Notification
    from echoui.components.progress_bar import ProgressBar
    from echoui.components.table_builder import TableBuilder
    from echoui.components.box_builder import BoxBuilder
    from echoui.components.spinner import Spinner
    from echoui.components.timer import Timer

    print("=" * 60)
    print("场景 1: 基础组件渲染验证")
    print("=" * 60)

    # 1. 通知
    n = Notification(normal_mode=True)
    out = n.success("操作成功完成").render()
    assert "[OK]" in out, f"通知失败: {out!r}"
    print(f"  [PASS] Notification.success: {out}")

    out = n.error("操作失败").render()
    assert "[X]" in out, f"错误通知失败: {out!r}"
    print(f"  [PASS] Notification.error: {out}")

    # 2. 进度条
    pb = ProgressBar(normal_mode=True, current=50, total=100)
    out = pb.render()
    assert "50" in out or "%" in out, f"进度条失败: {out!r}"
    print(f"  [PASS] ProgressBar: {out}")

    # 进度条链式调用
    pb2 = ProgressBar(normal_mode=True, current=0, total=100)
    out2 = pb2.advance(60).render()
    assert "60" in out2 or "%" in out2, f"进度条链式失败: {out2!r}"
    print(f"  [PASS] ProgressBar.advance: {out2}")

    # 3. 表格
    tb = TableBuilder(normal_mode=True)
    out = (
        tb.set_headers(["ID", "名称", "状态"])
        .add_row(["001", "测试项目", "完成"])
        .add_row(["002", "中文测试", "通过"])
        .render()
    )
    assert "测试项目" in out, f"表格失败: {out!r}"
    assert "中文测试" in out, f"表格CJK失败: {out!r}"
    print(f"  [PASS] TableBuilder (含CJK):")
    for line in out.split("\n"):
        print(f"         {line}")

    # 4. 盒子
    bb = BoxBuilder(normal_mode=True)
    out = bb.content("盒子内容测试").build()
    assert "盒子内容测试" in out, f"盒子失败: {out!r}"
    print(f"  [PASS] BoxBuilder: {repr(out[:50])}...")

    # 5. Spinner
    sp = Spinner(normal_mode=True)
    out = sp.render()
    assert isinstance(out, str), f"Spinner失败: {out!r}"
    print(f"  [PASS] Spinner: {out}")

    # 6. Timer
    tm = Timer(normal_mode=True)
    tm.start()
    out = tm.render()
    assert isinstance(out, str), f"Timer失败: {out!r}"
    tm.stop()
    print(f"  [PASS] Timer: {out}")

    print()
    return True


def verify_console_ui_flow() -> bool:
    """验证 ConsoleUI 链式调用流程。"""
    import io

    from echoui.components.console_ui import ConsoleUI

    print("=" * 60)
    print("场景 2: ConsoleUI 链式调用验证")
    print("=" * 60)

    # 捕获 stdout
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured

    try:
        ui = ConsoleUI(normal_mode=True)
        ui._output_stream = captured

        # 链式调用
        result = (
            ui.print("EchoUI 框架验证")
            .rule()
            .print("初始化组件...")
            .success("组件加载成功")
            .warning("注意: 测试模式")
            .newline()
        )

        assert result is ui, "链式调用未返回 self"
        print(f"  [PASS] ConsoleUI 链式调用返回 self", file=old_stdout)

        # 检查输出
        output = captured.getvalue()
        assert "EchoUI 框架验证" in output
        assert "[OK]" in output
        assert "[!]" in output
        line_count = output.strip().split("\n")
        print(f"  [PASS] ConsoleUI 输出累积: {len(line_count)} 行", file=old_stdout)

        # box 方法
        captured.truncate(0)
        captured.seek(0)
        ui2 = ConsoleUI(normal_mode=True)
        ui2._output_stream = captured
        ui2.box("盒子测试")
        out2 = captured.getvalue()
        assert "盒子测试" in out2
        print(f"  [PASS] ConsoleUI.box", file=old_stdout)

        # table 方法
        captured.truncate(0)
        captured.seek(0)
        ui3 = ConsoleUI(normal_mode=True)
        ui3._output_stream = captured
        ui3.table(
            headers=["列1", "列2"],
            rows=[["数据1", "数据2"]],
        )
        out3 = captured.getvalue()
        assert "数据1" in out3
        print(f"  [PASS] ConsoleUI.table (含CJK)", file=old_stdout)
    finally:
        sys.stdout = old_stdout

    print()
    return True


async def verify_async_components() -> bool:
    """验证异步组件：倒计时、异步输入、交互选择器。"""
    from echoui.components.countdown import Countdown
    from echoui.components.confirm_dialog import ConfirmDialog
    from echoui.components.stream_writer import StreamWriter

    print("=" * 60)
    print("场景 3: 异步组件验证")
    print("=" * 60)

    # 1. 倒计时（极短时间）
    tick_count = 0

    def on_tick(remaining: int) -> None:
        nonlocal tick_count
        tick_count += 1

    cd = Countdown(seconds=1, normal_mode=True, on_tick=on_tick)
    await cd.run()
    assert tick_count >= 1, f"倒计时未触发 tick: {tick_count}"
    print(f"  [PASS] Countdown: {tick_count} 次 tick")

    # 2. StreamWriter
    sw = StreamWriter()
    result = sw.write_text("流式输出测试").reset()
    assert result is sw, "StreamWriter 链式调用失败"
    print(f"  [PASS] StreamWriter 链式调用")

    # 3. ConfirmDialog (模拟)
    cd2 = ConfirmDialog(message="确定继续?")
    out = cd2.render()
    assert isinstance(out, str)
    print(f"  [PASS] ConfirmDialog render: {out[:50]}...")

    print()
    return True


def verify_theme_and_design_system() -> bool:
    """验证主题系统和设计令牌。"""
    from echoui.core.theme import Theme, ThemeConfig
    from echoui.core.layout import resolve_breakpoint, Breakpoint
    from echoui.core.typography import TYPE_SCALE_MAP
    from echoui.core.spacing import SPACING_MAP
    from echoui.core.design_tokens import RADIUS_MAP, SHADOW_MAP

    print("=" * 60)
    print("场景 4: 主题与设计系统验证")
    print("=" * 60)

    # 主题
    default = Theme.get("default")
    assert default.name == "default"
    print(f"  [PASS] Theme.get('default'): {default.name}")

    all_names = Theme.list_names()
    assert len(all_names) >= 9
    print(f"  [PASS] 内置主题数: {len(all_names)}")

    # 断点
    bp = resolve_breakpoint(800)
    assert bp.name == Breakpoint.XL
    print(f"  [PASS] resolve_breakpoint(800) = {bp.name.value}")

    # 排版
    assert len(TYPE_SCALE_MAP) == 8
    print(f"  [PASS] TYPE_SCALE_MAP: {len(TYPE_SCALE_MAP)} 种字号")

    # 间距
    assert len(SPACING_MAP) == 9
    print(f"  [PASS] SPACING_MAP: {len(SPACING_MAP)} 级间距")

    # 设计令牌
    assert len(RADIUS_MAP) == 7
    assert len(SHADOW_MAP) == 5
    print(f"  [PASS] RADIUS_MAP: {len(RADIUS_MAP)} 级圆角, SHADOW_MAP: {len(SHADOW_MAP)} 级阴影")

    print()
    return True


def verify_event_and_state() -> bool:
    """验证状态管理和事件总线。"""
    from echoui.core.state import State
    from echoui.core.event_bus import EventBus

    print("=" * 60)
    print("场景 5: 状态与事件总线验证")
    print("=" * 60)

    # State
    s = State[int](initial=0)
    values: list[int] = []
    s.add_listener(lambda v: values.append(v))
    s.set(42)
    assert s.get() == 42
    assert 42 in values
    print(f"  [PASS] State: get={s.get()}, listener收到{len(values)}次更新")

    # EventBus
    bus = EventBus()
    received: list[str] = []
    bus.subscribe("test_event", lambda data: received.append(data))
    bus.publish("test_event", "hello")
    assert "hello" in received
    print(f"  [PASS] EventBus: 订阅-发布，收到{len(received)}条消息")

    print()
    return True


def verify_cjk_handling() -> bool:
    """验证 CJK 字符宽度处理。"""
    from echoui.utils.text import get_display_width, truncate_to_width, pad_to_width

    print("=" * 60)
    print("场景 6: CJK 字符宽度处理验证")
    print("=" * 60)

    # 宽度计算
    assert get_display_width("Hello") == 5
    assert get_display_width("你好") == 4
    assert get_display_width("Hi你") == 4
    print(f"  [PASS] get_display_width: 'Hello'=5, '你好'=4, 'Hi你'=4")

    # 截断
    truncated = truncate_to_width("你好世界ABC", 6)
    assert get_display_width(truncated) <= 6
    print(f"  [PASS] truncate_to_width('你好世界ABC', 6) = '{truncated}' (宽度={get_display_width(truncated)})")

    # 填充
    padded = pad_to_width("中文", 8, align="left")
    assert get_display_width(padded) == 8
    print(f"  [PASS] pad_to_width('中文', 8, left) 宽度={get_display_width(padded)}")

    print()
    return True


def verify_platform_detection() -> bool:
    """验证平台检测和性能等级。"""
    from echoui.core.platform_detector import detect_performance_tier, PerformanceTier

    print("=" * 60)
    print("场景 7: 平台检测验证")
    print("=" * 60)

    tier = detect_performance_tier()
    assert isinstance(tier, PerformanceTier)
    print(f"  [PASS] detect_performance_tier() = {tier.name}")

    print()
    return True


async def main() -> None:
    """运行所有真实场景验证。"""
    results: dict[str, bool] = {}

    try:
        results["基础渲染"] = verify_basic_rendering()
    except Exception as e:
        print(f"  [FAIL] 基础渲染: {e}")
        results["基础渲染"] = False

    try:
        results["ConsoleUI"] = verify_console_ui_flow()
    except Exception as e:
        print(f"  [FAIL] ConsoleUI: {e}")
        results["ConsoleUI"] = False

    try:
        results["异步组件"] = await verify_async_components()
    except Exception as e:
        print(f"  [FAIL] 异步组件: {e}")
        results["异步组件"] = False

    try:
        results["主题设计系统"] = verify_theme_and_design_system()
    except Exception as e:
        print(f"  [FAIL] 主题设计系统: {e}")
        results["主题设计系统"] = False

    try:
        results["状态事件总线"] = verify_event_and_state()
    except Exception as e:
        print(f"  [FAIL] 状态事件总线: {e}")
        results["状态事件总线"] = False

    try:
        results["CJK处理"] = verify_cjk_handling()
    except Exception as e:
        print(f"  [FAIL] CJK处理: {e}")
        results["CJK处理"] = False

    try:
        results["平台检测"] = verify_platform_detection()
    except Exception as e:
        print(f"  [FAIL] 平台检测: {e}")
        results["平台检测"] = False

    print("=" * 60)
    print("真实场景验证总结")
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
        print("\n所有真实场景验证通过!")


if __name__ == "__main__":
    asyncio.run(main())
