from __future__ import annotations

from echoui.components.base_component import BaseComponent


class KeyValueList(BaseComponent):
    """键值对列表组件。

    以对齐的 ``key: value`` 格式渲染键值对，每行一对。
    支持通过 ``add()`` 方法链式添加条目。

    Examples:
        >>> kvl = KeyValueList()
        >>> result = kvl.add("name", "EchoUI").add("version", "1.0").render()
        >>> "name" in result and "EchoUI" in result
        True
    """

    def __init__(self) -> None:
        """初始化 KeyValueList 实例。"""
        super().__init__()
        self._items: dict[str, str] = {}

    def add(self, key: str, value: str) -> KeyValueList:
        """添加一个键值对到列表。

        Args:
            key: 键名。
            value: 对应的值。

        Returns:
            KeyValueList: 自身引用，支持链式调用。
        """
        self._items[key] = value
        return self

    def render(self) -> str:
        """渲染键值对列表，按键值对齐格式输出。

        计算最长键的长度以实现冒号对齐。

        Returns:
            str: 渲染后的键值对列表字符串。
        """
        if not self._items:
            return ""

        max_key_len = max(len(k) for k in self._items)
        lines: list[str] = []
        for key, value in self._items.items():
            padding = max_key_len - len(key)
            lines.append(f"{key}{' ' * padding}: {value}")
        return "\n".join(lines)
