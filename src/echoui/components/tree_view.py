from __future__ import annotations

from typing import Any

from echoui.components.base_component import BaseComponent


class TreeView(BaseComponent):
    """树形视图组件。

    以树形结构渲染嵌套字典数据，使用 Unicode 或 ASCII 缩进字符。
    正常模式下使用 ``+--`` 和 ``|``，彩色模式下使用 ``├──``, ``└──`` 和 ``│``。

    Examples:
        >>> tree = TreeView({"a": {"b": "c"}, "d": "e"}, normal_mode=True)
        >>> result = tree.render()
        >>> "a" in result and "b: c" in result and "d: e" in result
        True
    """

    # Unicode 树形字符
    BRANCH = "\u251c\u2500\u2500"  # ├──
    LAST_BRANCH = "\u2514\u2500\u2500"  # └──
    VERTICAL = "\u2502"  # │

    # ASCII 树形字符（正常模式）
    ASCII_BRANCH = "+--"
    ASCII_LAST_BRANCH = "+--"
    ASCII_VERTICAL = "|"

    def __init__(
        self,
        data: dict[str, Any] | None = None,
        normal_mode: bool = False,
    ) -> None:
        """初始化 TreeView 实例。

        Args:
            data: 嵌套字典表示的树形数据。
            normal_mode: 是否启用正常模式（无彩色输出）。
        """
        super().__init__(normal_mode=normal_mode)
        self._data: dict[str, Any] = data if data is not None else {}

    def render(self) -> str:
        """渲染树形结构数据。

        Returns:
            str: 渲染后的树形字符串。
        """
        if not self._data:
            return ""
        lines = self._render_node(self._data, prefix="", is_last=True)
        return "\n".join(lines)

    def _render_node(
        self,
        node: dict[str, Any],
        prefix: str,
        is_last: bool,
    ) -> list[str]:
        """递归渲染树节点。

        Args:
            node: 当前节点的字典数据。
            prefix: 前缀缩进字符串。
            is_last: 当前节点是否为最后一个兄弟节点。

        Returns:
            list[str]: 渲染后的行列表。
        """
        lines: list[str] = []
        keys = list(node.keys())

        for idx, key in enumerate(keys):
            value = node[key]
            is_current_last = idx == len(keys) - 1

            if isinstance(value, dict):
                branch_char = self._get_branch(is_current_last)
                lines.append(f"{prefix}{branch_char} {key}")
                child_prefix = self._get_child_prefix(prefix, is_current_last)
                lines.extend(self._render_node(value, child_prefix, is_current_last))
            else:
                branch_char = self._get_branch(is_current_last)
                lines.append(f"{prefix}{branch_char} {key}: {value}")

        return lines

    def _get_branch(self, is_last: bool) -> str:
        """获取当前节点的分支字符。

        Args:
            is_last: 是否为最后一个节点。

        Returns:
            str: 分支字符。
        """
        if self._normal_mode:
            return self.ASCII_BRANCH if not is_last else self.ASCII_LAST_BRANCH
        return self.BRANCH if not is_last else self.LAST_BRANCH

    def _get_child_prefix(self, prefix: str, is_last: bool) -> str:
        """获取子节点的前缀缩进。

        Args:
            prefix: 当前前缀。
            is_last: 当前节点是否为最后一个。

        Returns:
            str: 子节点的新前缀。
        """
        if self._normal_mode:
            connector = "   " if is_last else f" {self.ASCII_VERTICAL} "
        else:
            connector = "    " if is_last else f" {self.VERTICAL} "
        return prefix + connector
