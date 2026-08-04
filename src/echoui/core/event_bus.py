from __future__ import annotations

from typing import Any, Callable


class EventBus:
    """轻量级事件总线，支持按事件名订阅、发布和清除处理器。

    采用同步调用模型，``publish()`` 会依次调用该事件下所有已注册的处理器。
    适用于模块间解耦通信，如主题变更通知、生命周期事件广播等。

    Examples:
        >>> bus = EventBus()
        >>> results: list[str] = []
        >>> bus.subscribe("greet", lambda name: results.append(f"Hello, {name}!"))
        >>> bus.publish("greet", "World")
        >>> results
        ['Hello, World!']
    """

    def __init__(self) -> None:
        """初始化 EventBus 实例。"""
        self._handlers: dict[str, list[Callable[..., None]]] = {}

    def subscribe(self, event: str, handler: Callable[..., None]) -> None:
        """为指定事件注册一个处理器。

        同一处理器可以重复注册到同一事件，发布时会被调用多次。

        Args:
            event: 事件名称，用于标识一类事件。
            handler: 事件触发时将被调用的可调用对象。

        Examples:
            >>> bus = EventBus()
            >>> bus.subscribe("click", lambda: None)
            >>> "click" in bus._handlers
            True
        """
        if event not in self._handlers:
            self._handlers[event] = []
        self._handlers[event].append(handler)

    def unsubscribe(self, event: str, handler: Callable[..., None]) -> None:
        """移除指定事件的某个处理器。

        如果事件不存在或处理器未注册，则不执行任何操作。

        Args:
            event: 事件名称。
            handler: 要移除的处理器引用。

        Examples:
            >>> bus = EventBus()
            >>> fn = lambda: None
            >>> bus.subscribe("click", fn)
            >>> bus.unsubscribe("click", fn)
            >>> bus._handlers.get("click")
            []
        """
        if event in self._handlers:
            if handler in self._handlers[event]:
                self._handlers[event].remove(handler)

    def publish(self, event: str, *args: Any, **kwargs: Any) -> None:
        """发布事件，依次调用所有已注册的处理器。

        处理器按照注册顺序同步执行。如果某个处理器抛出异常，
        后续处理器仍会继续调用。

        Args:
            event: 要发布的事件名称。
            *args: 传递给处理器的位置参数。
            **kwargs: 传递给处理器的关键字参数。

        Examples:
            >>> bus = EventBus()
            >>> collected: list[tuple] = []
            >>> bus.subscribe("data", lambda x, y=0: collected.append((x, y)))
            >>> bus.publish("data", 1, y=2)
            >>> collected
            [(1, 2)]
        """
        if event not in self._handlers:
            return
        for handler in list(self._handlers[event]):
            handler(*args, **kwargs)

    def clear(self) -> None:
        """清除所有事件及其处理器。

        调用后事件总线回到初始空状态。

        Examples:
            >>> bus = EventBus()
            >>> bus.subscribe("test", lambda: None)
            >>> bus.clear()
            >>> bus._handlers
            {}
        """
        self._handlers.clear()
