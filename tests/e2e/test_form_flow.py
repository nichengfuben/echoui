from __future__ import annotations

import pytest

from echoui.components.box_builder import BoxBuilder
from echoui.components.console_ui import ConsoleUI
from echoui.components.key_value_list import KeyValueList
from echoui.components.notification import Notification
from echoui.components.table_builder import TableBuilder


class TestFormFlow:
    """端到端表单填写流程测试。

    覆盖：表单显示 -> 数据输入 -> 数据验证 -> 提交反馈 完整链路。
    """

    def test_form_display_with_box(self) -> None:
        """BoxBuilder 应用于表单容器显示。"""
        builder = BoxBuilder(normal_mode=True)
        result = (
            builder.title("用户注册表单")
            .content("姓名: __________\n邮箱: __________\n年龄: __")
            .build()
        )
        assert "用户注册表单" in result
        assert "姓名" in result
        assert "邮箱" in result

    def test_form_data_as_key_value(self) -> None:
        """KeyValueList 应用于表单数据展示。"""
        kvl = KeyValueList()
        result = (
            kvl.add("姓名", "张三")
            .add("邮箱", "zhang@example.com")
            .add("年龄", "25")
            .add("城市", "北京")
            .render()
        )
        assert "姓名" in result
        assert "张三" in result
        assert "邮箱" in result
        assert "zhang@example.com" in result

    def test_form_validation_feedback(self) -> None:
        """Notification 应用于表单验证反馈。"""
        # 成功反馈
        success = Notification(normal_mode=True).success("表单提交成功").render()
        assert "OK" in success

        # 错误反馈
        error = Notification(normal_mode=True).error("邮箱格式无效").render()
        assert "X" in error

        # 警告反馈
        warning = Notification(normal_mode=True).warning("姓名为必填项").render()
        assert "WARN" in warning or "!" in warning

    def test_form_data_in_table(self) -> None:
        """TableBuilder 应用于表单数据汇总。"""
        builder = TableBuilder(normal_mode=True)
        result = (
            builder.set_headers(["字段", "值"])
            .add_row(["姓名", "张三"])
            .add_row(["邮箱", "test@example.com"])
            .add_row(["手机号", "13800138000"])
            .render()
        )
        assert "字段" in result
        assert "姓名" in result
        assert "张三" in result
        assert "test@example.com" in result

    def test_full_form_submission_flow(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """完整表单提交流程：展示 -> 确认 -> 反馈。"""
        ui = ConsoleUI(normal_mode=True)

        # 1. 展示表单
        ui.print("=== 用户注册 ===")

        # 2. 显示表单数据
        kvl = KeyValueList()
        kvl.add("姓名", "李四")
        kvl.add("邮箱", "lisi@example.com")
        ui.print(kvl.render())

        # 3. 提交反馈
        ui.success("注册成功")

        captured = capsys.readouterr()
        assert "用户注册" in captured.out
        assert "李四" in captured.out
        assert "lisi@example.com" in captured.out
        assert "成功" in captured.out

    def test_form_with_cjk_content(self) -> None:
        """表单中的 CJK 内容应正确显示。"""
        kvl = KeyValueList()
        result = (
            kvl.add("姓名", "王五")
            .add("地址", "北京市朝阳区")
            .add("备注", "VIP 客户")
            .render()
        )
        assert "姓名" in result
        assert "王五" in result
        assert "地址" in result
        assert "北京市朝阳区" in result
        assert "备注" in result
        assert "VIP 客户" in result

    def test_multi_step_form_flow(self) -> None:
        """多步骤表单流程。"""
        # Step 1: 基本信息
        step1 = KeyValueList().add("姓名", "赵六").add("年龄", "30").render()
        assert "姓名" in step1

        # Step 2: 联系方式
        step2 = (
            KeyValueList()
            .add("邮箱", "zhao@example.com")
            .add("手机", "13900139000")
            .render()
        )
        assert "邮箱" in step2

        # Step 3: 确认提交
        confirmation = (
            BoxBuilder(normal_mode=True)
            .title("确认信息")
            .content("请确认以上信息")
            .build()
        )
        assert "确认信息" in confirmation

        # 提交结果
        result = Notification(normal_mode=True).success("多步骤表单提交完成").render()
        assert "完成" in result
