from __future__ import annotations

import pytest

from echoui.components.box_builder import BoxBuilder
from echoui.components.console_ui import ConsoleUI
from echoui.components.notification import Notification
from echoui.components.table_builder import TableBuilder


class TestChatFlow:
    """端到端聊天会话流程测试。"""

    def test_console_ui_chain_print(self, capsys: pytest.CaptureFixture) -> None:
        """ConsoleUI 应支持链式 print 调用。"""
        ui = ConsoleUI(normal_mode=True)
        ui.print("Hello").print("World")
        captured = capsys.readouterr()
        assert "Hello" in captured.out
        assert "World" in captured.out

    def test_console_ui_chain_with_newline(self, capsys: pytest.CaptureFixture) -> None:
        """ConsoleUI 链式调用应包含 newline。"""
        ui = ConsoleUI(normal_mode=True)
        ui.print("Line 1").newline().print("Line 2")
        captured = capsys.readouterr()
        assert "Line 1" in captured.out
        assert "Line 2" in captured.out

    def test_console_ui_box_output(self, capsys: pytest.CaptureFixture) -> None:
        """ConsoleUI.box() 应输出带框的内容。"""
        ui = ConsoleUI(normal_mode=True)
        ui.box("Hello World", title="Test")
        captured = capsys.readouterr()
        assert "Hello World" in captured.out

    def test_console_ui_table_output(self, capsys: pytest.CaptureFixture) -> None:
        """ConsoleUI.table() 应输出格式化的表格。"""
        ui = ConsoleUI(normal_mode=True)
        ui.table(
            headers=["ID", "Name"],
            rows=[["1", "Alice"], ["2", "Bob"]],
        )
        captured = capsys.readouterr()
        assert "ID" in captured.out
        assert "Alice" in captured.out
        assert "Bob" in captured.out

    def test_console_ui_notifications(self, capsys: pytest.CaptureFixture) -> None:
        """ConsoleUI 应支持所有类型的通知。"""
        ui = ConsoleUI(normal_mode=True)
        ui.success("OK").warning("Warn").error("Err").info("Info")
        captured = capsys.readouterr()
        assert "OK" in captured.out
        assert "Warn" in captured.out
        assert "Err" in captured.out
        assert "Info" in captured.out

    def test_console_ui_rule(self, capsys: pytest.CaptureFixture) -> None:
        """ConsoleUI.rule() 应输出分隔线。"""
        ui = ConsoleUI(normal_mode=True)
        ui.rule(char="-", width=20)
        captured = capsys.readouterr()
        assert "-" * 20 in captured.out


class TestFormFlow:
    """端到端表单填写流程测试。"""

    def test_box_builder_form_display(self) -> None:
        """BoxBuilder 应用于表单显示。"""
        builder = BoxBuilder(normal_mode=True)
        result = builder.title("User Form").content("Name: John\nAge: 30").build()
        assert "User Form" in result
        assert "Name: John" in result
        assert "Age: 30" in result

    def test_table_builder_data_display(self) -> None:
        """TableBuilder 应正确显示表单数据。"""
        builder = TableBuilder(normal_mode=True)
        result = (
            builder.set_headers(["Field", "Value"])
            .add_row(["Name", "张三"])
            .add_row(["Email", "test@example.com"])
            .render()
        )
        assert "Field" in result
        assert "Name" in result
        assert "张三" in result
        assert "Email" in result

    def test_key_value_form_display(self) -> None:
        """KeyValueList 应用于键值表单显示。"""
        from echoui.components.key_value_list import KeyValueList

        kvl = KeyValueList()
        result = kvl.add("姓名", "张三").add("年龄", "30").add("城市", "北京").render()
        assert "姓名" in result
        assert "张三" in result
        assert "年龄" in result
        assert "城市" in result

    def test_notification_form_feedback(self) -> None:
        """Notification 应用于表单提交反馈。"""
        notif = Notification(normal_mode=True)
        success_result = notif.success("表单提交成功").render()
        assert "OK" in success_result

        error_notif = Notification(normal_mode=True)
        error_result = error_notif.error("表单验证失败").render()
        assert "X" in error_result


class TestFullPipeline:
    """完整流水线测试：ConsoleUI + BoxBuilder + TableBuilder + Notification。"""

    def test_full_chain(self, capsys: pytest.CaptureFixture) -> None:
        """完整链式调用应正常工作。"""
        ui = ConsoleUI(normal_mode=True)
        ui.rule("=").print("Dashboard").rule("=").newline()
        ui.box("Welcome to EchoUI", title="Header")
        ui.table(
            headers=["Metric", "Value"],
            rows=[["Users", "100"], ["Requests", "1000"]],
        )
        ui.success("Data loaded successfully")
        captured = capsys.readouterr()
        assert "Dashboard" in captured.out
        assert "Welcome to EchoUI" in captured.out
        assert "Users" in captured.out
        assert "Data loaded successfully" in captured.out

    def test_cjk_content_in_table(self, capsys: pytest.CaptureFixture) -> None:
        """表格中的 CJK 字符应正确显示。"""
        ui = ConsoleUI(normal_mode=True)
        ui.table(
            headers=["姓名", "城市"],
            rows=[["张三", "北京"], ["李四", "上海"]],
        )
        captured = capsys.readouterr()
        assert "张三" in captured.out
        assert "北京" in captured.out
        assert "李四" in captured.out
        assert "上海" in captured.out
