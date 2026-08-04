from __future__ import annotations

import io

from echoui import EchoUI, echoui


class TestEchouiFunction:
    """echoui() 工厂函数测试。"""

    def test_returns_echoui_instance(self) -> None:
        """应返回 EchoUI 实例。"""
        ui = echoui(normal_mode=True)
        assert isinstance(ui, EchoUI)

    def test_default_normal_mode_false(self) -> None:
        """默认 normal_mode 为 False。"""
        ui = echoui()
        assert ui._normal_mode is False

    def test_normal_mode_true(self) -> None:
        """normal_mode=True 应正确设置。"""
        ui = echoui(normal_mode=True)
        assert ui._normal_mode is True


class TestEchoUIChain:
    """EchoUI 链式调用测试。"""

    def test_all_methods_return_self(self) -> None:
        """所有方法应返回 self。"""
        ui = echoui(normal_mode=True)
        assert ui.title("Hi") is ui
        assert ui.rule() is ui
        assert ui.newline() is ui
        assert ui.success("OK") is ui
        assert ui.warning("Warn") is ui
        assert ui.error("Err") is ui
        assert ui.info("Info") is ui
        assert ui.box("content") is ui
        assert ui.table(["H"], [["A"]]) is ui
        assert ui.block("OK") is ui
        assert ui.progress(5, 10) is ui
        assert ui.kv(a="1") is ui
        assert ui.tree({"a": "b"}) is ui
        assert ui.print() is ui
        assert ui.clear() is ui


class TestEchoUIOutput:
    """EchoUI 输出测试。"""

    def test_print_flushes_to_stream(self) -> None:
        """print() 应刷新到输出流。"""
        stream = io.StringIO()
        ui = echoui(normal_mode=True, stream=stream)
        ui.title("Hello").print()
        assert "Hello" in stream.getvalue()

    def test_clear_removes_buffer(self) -> None:
        """clear() 应清空缓冲区。"""
        stream = io.StringIO()
        ui = echoui(normal_mode=True, stream=stream)
        ui.title("Hello").clear().print()
        assert stream.getvalue() == ""

    def test_block_renders_six_lines(self) -> None:
        """block() 应渲染 6 行。"""
        stream = io.StringIO()
        ui = echoui(normal_mode=True, stream=stream)
        ui.block("OK").print()
        lines = stream.getvalue().strip().split("\n")
        assert len(lines) == 6

    def test_table_renders(self) -> None:
        """table() 应渲染表格。"""
        stream = io.StringIO()
        ui = echoui(normal_mode=True, stream=stream)
        ui.table(["Name"], [["Test"]]).print()
        assert "Test" in stream.getvalue()

    def test_kv_renders(self) -> None:
        """kv() 应渲染键值对。"""
        stream = io.StringIO()
        ui = echoui(normal_mode=True, stream=stream)
        ui.kv(name="EchoUI", version="2.0.0").print()
        output = stream.getvalue()
        assert "name" in output
        assert "EchoUI" in output

    def test_tree_renders(self) -> None:
        """tree() 应渲染树形结构。"""
        stream = io.StringIO()
        ui = echoui(normal_mode=True, stream=stream)
        ui.tree({"a": {"b": "c"}}).print()
        output = stream.getvalue()
        assert "a" in output

    def test_box_renders(self) -> None:
        """box() 应渲染框体。"""
        stream = io.StringIO()
        ui = echoui(normal_mode=True, stream=stream)
        ui.box("content", title="Title").print()
        output = stream.getvalue()
        assert "Title" in output
        assert "content" in output

    def test_progress_renders(self) -> None:
        """progress() 应渲染进度条。"""
        stream = io.StringIO()
        ui = echoui(normal_mode=True, stream=stream)
        ui.progress(50, 100).print()
        assert "50" in stream.getvalue() or "%" in stream.getvalue()

    def test_notifications_render(self) -> None:
        """通知方法应正确渲染。"""
        stream = io.StringIO()
        ui = echoui(normal_mode=True, stream=stream)
        ui.success("OK").warning("W").error("E").info("I").print()
        output = stream.getvalue()
        assert "[OK]" in output
        assert "[!]" in output
        assert "[X]" in output
        assert "[i]" in output


class TestEchoUIComplexWorkflow:
    """EchoUI 复杂工作流测试。"""

    def test_full_dashboard(self) -> None:
        """完整 Dashboard 渲染。"""
        stream = io.StringIO()
        ui = echoui(normal_mode=True, stream=stream)
        (
            ui.rule("=", 40)
            .title("Dashboard")
            .rule("=", 40)
            .newline()
            .block("OK")
            .newline()
            .kv(app="EchoUI", status="Running")
            .newline()
            .table(["Module", "Status"], [["core", "OK"]])
            .newline()
            .success("All good")
            .rule("=", 40)
            .print()
        )
        output = stream.getvalue()
        assert "Dashboard" in output
        assert "OK" in output or len(output.split("\n")) > 10
        assert "[OK]" in output
        assert "All good" in output

    def test_chained_without_print(self) -> None:
        """链式调用不 print 时不应有输出。"""
        stream = io.StringIO()
        ui = echoui(normal_mode=True, stream=stream)
        ui.title("Hello").success("World")
        assert stream.getvalue() == ""
