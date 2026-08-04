from __future__ import annotations


class EchoError(Exception):
    """EchoUI 框架异常基类。

    所有框架级异常必须继承此类，便于用户统一捕获。

    Examples:
        >>> try:
        ...     raise EchoError("test")
        ... except EchoError as e:
        ...     str(e)
        'test'
    """


class ConfigError(EchoError):
    """配置错误：主题、组件参数、环境变量验证失败。

    Examples:
        >>> try:
        ...     raise ConfigError("无效配置")
        ... except ConfigError as e:
        ...     str(e)
        '无效配置'
    """


class RenderError(EchoError):
    """渲染错误：ANSI 输出、HTML 生成、布局计算失败。

    Examples:
        >>> try:
        ...     raise RenderError("渲染失败")
        ... except RenderError as e:
        ...     str(e)
        '渲染失败'
    """


class AdapterError(EchoError):
    """适配器错误：后端连接、路由注册、响应发送失败。

    Examples:
        >>> try:
        ...     raise AdapterError("连接失败")
        ... except AdapterError as e:
        ...     str(e)
        '连接失败'
    """


class InputError(EchoError):
    """输入错误：用户输入验证、IME 处理、文件上传校验失败。

    Examples:
        >>> try:
        ...     raise InputError("输入非法")
        ... except InputError as e:
        ...     str(e)
        '输入非法'
    """
