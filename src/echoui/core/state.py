from __future__ import annotations

from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class State(Generic[T]):
    """泛型状态容器，支持值变更监听与自动通知。

    适用于需要在值变化时触发回调的场景，如主题切换、配置更新等。
    监听器在 ``set()`` 调用时同步执行。

    Args:
        initial: 状态的初始值。

    Examples:
        >>> state = State(0)
        >>> state.get()
        0
        >>> state.set(42)
        >>> state.get()
        42
    """

    def __init__(self, initial: T) -> None:
        """初始化 State 实例。

        Args:
            initial: 状态的初始值。
        """
        self._value: T = initial
        self._listeners: list[Callable[[T], None]] = []

    def get(self) -> T:
        """获取当前状态值。

        Returns:
            当前存储的状态值。

        Examples:
            >>> state = State("hello")
            >>> state.get()
            'hello'
        """
        return self._value

    def set(self, value: T) -> None:
        """更新状态值并通知所有已注册的监听器。

        监听器按照注册顺序依次同步调用。如果监听器抛出异常，
        后续监听器仍会继续执行。

        Args:
            value: 新的状态值。

        Examples:
            >>> results: list[int] = []
            >>> state = State(0)
            >>> state.add_listener(lambda v: results.append(v))
            >>> state.set(10)
            >>> results
            [10]
        """
        self._value = value
        self._notify(value)

    def add_listener(self, callback: Callable[[T], None]) -> None:
        """注册一个状态变更监听器。

        同一回调函数可以重复注册，每次 ``set()`` 都会被调用多次。

        Args:
            callback: 接受新状态值作为参数的可调用对象。

        Examples:
            >>> state = State(1)
            >>> state.add_listener(print)  # doctest: +SKIP
        """
        self._listeners.append(callback)

    def remove_listener(self, callback: Callable[[T], None]) -> None:
        """移除一个已注册的监听器。

        如果回调函数未注册，则不执行任何操作。

        Args:
            callback: 要移除的回调函数引用。

        Examples:
            >>> state = State(0)
            >>> fn = lambda v: None
            >>> state.add_listener(fn)
            >>> state.remove_listener(fn)
            >>> state._listeners
            []
        """
        if callback in self._listeners:
            self._listeners.remove(callback)

    def _notify(self, value: T) -> None:
        """同步调用所有已注册的监听器。

        Args:
            value: 传递给监听器的状态值。
        """
        for listener in list(self._listeners):
            listener(value)
