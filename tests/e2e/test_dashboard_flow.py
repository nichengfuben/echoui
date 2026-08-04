from __future__ import annotations

import pytest

from echoui.components.block_art import BlockArt
from echoui.components.box_builder import BoxBuilder
from echoui.components.console_ui import ConsoleUI
from echoui.components.notification import Notification
from echoui.components.progress_bar import ProgressBar
from echoui.components.spinner import Spinner
from echoui.components.table_builder import TableBuilder


class TestDashboardFlow:
    """端到端仪表盘流程测试。

    覆盖：标题 -> 统计卡片 -> 数据表格 -> 进度条 -> 通知 完整链路。
    """

    def test_dashboard_header(self) -> None:
        """BlockArt 应用于仪表盘标题。"""
        art = BlockArt(text="EchoUI", normal_mode=True)
        result = art.render()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_dashboard_statistics_box(self) -> None:
        """BoxBuilder 应用于统计卡片。"""
        builder = BoxBuilder(normal_mode=True)
        result = (
            builder.title("统计概览")
            .content("活跃用户: 1,234\n今日访问: 5,678\n转化率: 3.45%")
            .build()
        )
        assert "统计概览" in result
        assert "活跃用户" in result
        assert "1,234" in result

    def test_dashboard_data_table(self) -> None:
        """TableBuilder 应用于仪表盘数据表格。"""
        builder = TableBuilder(normal_mode=True)
        result = (
            builder.set_headers(["指标", "数值", "趋势"])
            .add_row(["活跃用户", "1,234", "+5.2%"])
            .add_row(["今日访问", "5,678", "+12.1%"])
            .add_row(["转化率", "3.45%", "-0.3%"])
            .render()
        )
        assert "指标" in result
        assert "活跃用户" in result
        assert "1,234" in result
        assert "5,678" in result
        assert "3.45%" in result

    def test_dashboard_progress_bar(self) -> None:
        """ProgressBar 应用于仪表盘进度展示。"""
        p = ProgressBar(current=75, total=100, normal_mode=True, message="服务器负载")
        result = p.render()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_dashboard_notifications(self) -> None:
        """Notification 应用于仪表盘状态通知。"""
        notifications = [
            Notification(normal_mode=True).success("系统运行正常").render(),
            Notification(normal_mode=True).warning("磁盘空间不足").render(),
            Notification(normal_mode=True).error("数据库连接失败").render(),
            Notification(normal_mode=True).info("新版本可用").render(),
        ]
        # 至少有一个通知包含预期文本
        combined = "\n".join(notifications)
        assert "正常" in combined or "OK" in combined

    def test_full_dashboard_pipeline(self, capsys: pytest.CaptureFixture[str]) -> None:
        """完整仪表盘流水线：标题 -> 统计 -> 表格 -> 进度 -> 通知。"""
        ui = ConsoleUI(normal_mode=True)

        # 1. 标题
        ui.print("Dashboard v1.0").rule("=")

        # 2. 统计卡片
        stats_box = (
            BoxBuilder(normal_mode=True)
            .title("Overview")
            .content("Users: 100\nRequests: 1000")
            .build()
        )
        ui.print(stats_box)

        # 3. 数据表格
        ui.table(
            headers=["Metric", "Value", "Trend"],
            rows=[
                ["Users", "100", "+10%"],
                ["Requests", "1000", "+25%"],
                ["Errors", "5", "-2%"],
            ],
        )

        # 4. 进度条
        p = ProgressBar(current=80, total=100, normal_mode=True, message="CPU Usage")
        ui.print(p.render())

        # 5. 通知
        ui.success("All systems operational")

        captured = capsys.readouterr()
        assert "Dashboard" in captured.out
        assert "Overview" in captured.out
        assert "Users" in captured.out
        assert "100" in captured.out
        assert "Requests" in captured.out
        assert "operational" in captured.out

    def test_dashboard_with_cjk_content(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """仪表盘中的中文内容应正确显示。"""
        ui = ConsoleUI(normal_mode=True)

        ui.print("中文仪表盘").rule("=")

        kvl_content = "活跃用户: 1234\n今日访问: 5678"
        box = BoxBuilder(normal_mode=True).title("统计").content(kvl_content).build()
        ui.print(box)

        ui.table(
            headers=["指标", "数值"],
            rows=[["活跃用户", "1234"], ["今日访问", "5678"]],
        )

        ui.success("数据加载完成")

        captured = capsys.readouterr()
        assert "中文仪表盘" in captured.out
        assert "活跃用户" in captured.out
        assert "1234" in captured.out
        assert "数据加载完成" in captured.out

    def test_spinner_in_dashboard(self) -> None:
        """Spinner 可在仪表盘中表示加载状态。"""
        spinner = Spinner(normal_mode=True)
        # Spinner 的 render 方法应返回字符串
        result = spinner.render()
        assert isinstance(result, str)
        assert len(result) > 0
