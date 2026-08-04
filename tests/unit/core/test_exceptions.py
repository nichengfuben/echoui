from __future__ import annotations

import pytest

from echoui.core.exceptions import (
    AdapterError,
    ConfigError,
    EchoError,
    InputError,
    RenderError,
)


class TestEchoError:
    """EchoError 基类测试。"""

    def test_echo_error_is_exception(self) -> None:
        """EchoError 应为 Exception 的子类。"""
        assert issubclass(EchoError, Exception)

    def test_echo_error_can_be_raised(self) -> None:
        """EchoError 应可被抛出。"""
        with pytest.raises(EchoError):
            raise EchoError("测试异常")

    def test_echo_error_message(self) -> None:
        """EchoError 应携带错误消息。"""
        with pytest.raises(EchoError, match="自定义错误"):
            raise EchoError("自定义错误")


class TestConfigError:
    """ConfigError 配置错误测试。"""

    def test_config_error_is_echo_error(self) -> None:
        """ConfigError 应继承自 EchoError。"""
        assert issubclass(ConfigError, EchoError)

    def test_config_error_can_be_raised(self) -> None:
        """ConfigError 应可被抛出。"""
        with pytest.raises(ConfigError, match="配置无效"):
            raise ConfigError("配置无效")


class TestRenderError:
    """RenderError 渲染错误测试。"""

    def test_render_error_is_echo_error(self) -> None:
        """RenderError 应继承自 EchoError。"""
        assert issubclass(RenderError, EchoError)

    def test_render_error_can_be_raised(self) -> None:
        """RenderError 应可被抛出。"""
        with pytest.raises(RenderError, match="渲染失败"):
            raise RenderError("渲染失败")


class TestAdapterError:
    """AdapterError 适配器错误测试。"""

    def test_adapter_error_is_echo_error(self) -> None:
        """AdapterError 应继承自 EchoError。"""
        assert issubclass(AdapterError, EchoError)

    def test_adapter_error_can_be_raised(self) -> None:
        """AdapterError 应可被抛出。"""
        with pytest.raises(AdapterError, match="连接失败"):
            raise AdapterError("连接失败")


class TestInputError:
    """InputError 输入错误测试。"""

    def test_input_error_is_echo_error(self) -> None:
        """InputError 应继承自 EchoError。"""
        assert issubclass(InputError, EchoError)

    def test_input_error_can_be_raised(self) -> None:
        """InputError 应可被抛出。"""
        with pytest.raises(InputError, match="输入格式错误"):
            raise InputError("输入格式错误")


class TestExceptionHierarchy:
    """异常层次结构测试。"""

    def test_all_exceptions_are_echo_error(self) -> None:
        """所有自定义异常都应能被 EchoError 捕获。"""
        for exc_class in (ConfigError, RenderError, AdapterError, InputError):
            with pytest.raises(EchoError):
                raise exc_class("测试")

    def test_specific_exception_is_caught(self) -> None:
        """具体异常应被精确捕获。"""
        with pytest.raises(ConfigError):
            raise ConfigError("配置错误")
        with pytest.raises(RenderError):
            raise RenderError("渲染错误")
        with pytest.raises(AdapterError):
            raise AdapterError("适配器错误")
        with pytest.raises(InputError):
            raise InputError("输入错误")
