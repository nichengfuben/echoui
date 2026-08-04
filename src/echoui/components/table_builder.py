from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from echoui.components.base_component import BaseComponent
from echoui.core.exceptions import ConfigError
from echoui.utils.text import get_display_width, pad_to_width

if TYPE_CHECKING:
    from echoui.core.renderer import GradientRenderer
    from echoui.core.theme import ThemeConfig


class TableBuilder(BaseComponent):
    """表格构建组件，用于渲染带表头和数据的文本表格。

    支持设置表头、添加数据行、配置列对齐方式，
    使用 get_display_width 正确处理 CJK 字符宽度。

    Examples:
        >>> t = TableBuilder(normal_mode=True)
        >>> _ = t.set_headers(["姓名", "年龄"]).add_row(["张三", "25"])
        >>> result = t.render()
        >>> "张三" in result and "25" in result
        True
    """

    def __init__(
        self,
        renderer: Optional[GradientRenderer] = None,
        normal_mode: bool = False,
        theme: Optional[ThemeConfig] = None,
    ) -> None:
        """初始化表格构建组件。

        Args:
            renderer: 渐变渲染器实例。
            normal_mode: 是否启用正常模式。
            theme: 主题配置。
        """
        super().__init__(renderer=renderer, normal_mode=normal_mode, theme=theme)
        self._headers: list[str] = []
        self._rows: list[list[str]] = []
        self._alignments: list[str] = []

    def set_headers(self, headers: list[str]) -> TableBuilder:
        """设置表格表头。

        Args:
            headers: 表头文本列表。

        Returns:
            TableBuilder: 组件自身，支持链式调用。
        """
        self._headers = list(headers)
        if not self._alignments:
            self._alignments = ["left"] * len(self._headers)
        return self

    def add_row(self, row: list[str]) -> TableBuilder:
        """添加一行数据。

        Args:
            row: 单元格文本列表，长度必须与表头一致。

        Returns:
            TableBuilder: 组件自身，支持链式调用。

        Raises:
            ConfigError: 当行长度与表头长度不匹配时抛出。
        """
        if len(row) != len(self._headers):
            raise ConfigError(
                f"行长度 {len(row)} 与表头长度 {len(self._headers)} 不匹配"
            )
        self._rows.append(list(row))
        return self

    def set_alignments(self, alignments: list[str]) -> TableBuilder:
        """设置列对齐方式。

        Args:
            alignments: 对齐方式列表，每项为 "left"/"center"/"right"。

        Returns:
            TableBuilder: 组件自身，支持链式调用。

        Raises:
            ConfigError: 当对齐方式非法或长度不匹配时抛出。
        """
        valid = {"left", "center", "right"}
        for align in alignments:
            if align not in valid:
                raise ConfigError(f"非法对齐方式: {align!r}，可选: {sorted(valid)}")
        if len(alignments) != len(self._headers):
            raise ConfigError(
                f"对齐方式长度 {len(alignments)} 与表头长度 {len(self._headers)} 不匹配"
            )
        self._alignments = list(alignments)
        return self

    def render(self) -> str:
        """渲染表格。

        生成包含表头行、分隔线和数据行的表格字符串。
        列宽由该列所有单元格的最大显示宽度决定。

        Returns:
            str: 渲染后的表格字符串。
        """
        if not self._headers:
            return ""

        col_count = len(self._headers)
        col_widths: list[int] = [get_display_width(h) for h in self._headers]

        for row in self._rows:
            for i in range(col_count):
                cell_width = get_display_width(row[i])
                if cell_width > col_widths[i]:
                    col_widths[i] = cell_width

        separator = "-+-".join("-" * w for w in col_widths)

        header_cells = []
        for i, header in enumerate(self._headers):
            align = self._alignments[i] if i < len(self._alignments) else "left"
            header_cells.append(pad_to_width(header, col_widths[i], align))
        header_line = " | ".join(header_cells)

        lines = [header_line, separator]

        for row in self._rows:
            cells = []
            for i in range(col_count):
                align = self._alignments[i] if i < len(self._alignments) else "left"
                cells.append(pad_to_width(row[i], col_widths[i], align))
            lines.append(" | ".join(cells))

        return "\n".join(lines)
