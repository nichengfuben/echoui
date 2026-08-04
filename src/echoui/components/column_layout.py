from __future__ import annotations

from echoui.components.base_component import BaseComponent


class ColumnLayout(BaseComponent):
    """列布局组件。

    将多个内容字符串并排渲染为列，每列之间用空格分隔。
    所有行按最高列的高度对齐，不足高度的列用空行填充。

    Examples:
        >>> cols = ColumnLayout(["a\\nb", "x\\ny\\nz"])
        >>> print(cols.render())
        a  x
        b  y
           z
    """

    COLUMN_GAP = 2

    def __init__(self, columns: list[str] | None = None) -> None:
        """初始化 ColumnLayout 实例。

        Args:
            columns: 每列内容的字符串列表。
        """
        super().__init__()
        self._columns: list[str] = columns if columns is not None else []

    def render(self) -> str:
        """并排渲染所有列。

        按最高列的行数对齐，短列用空白行补齐。

        Returns:
            str: 渲染后的列布局字符串。
        """
        if not self._columns:
            return ""

        split_columns = [col.split("\n") for col in self._columns]
        max_rows = max(len(col) for col in split_columns)
        col_widths = [
            max((len(line) for line in col), default=0) for col in split_columns
        ]

        lines: list[str] = []
        for row_idx in range(max_rows):
            row_parts: list[str] = []
            for col_idx, col_lines in enumerate(split_columns):
                if row_idx < len(col_lines):
                    line = col_lines[row_idx]
                else:
                    line = ""
                padding = col_widths[col_idx] - len(line)
                row_parts.append(line + " " * padding)
            lines.append((" " * self.COLUMN_GAP).join(row_parts))

        return "\n".join(lines)
