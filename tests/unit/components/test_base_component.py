from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from echoui.components.base_component import BaseComponent
from echoui.core.renderer import GradientRenderer


class _ConcreteComponent(BaseComponent):
    """Concrete subclass of BaseComponent for testing."""

    def render(self) -> str:
        return "concrete"


class _BrokenComponent(BaseComponent):
    """Concrete subclass that does NOT implement render (for abstract test)."""

    pass  # pragma: no cover


class TestBaseComponent:
    """Tests for BaseComponent class."""

    def test_creates_with_defaults(self) -> None:
        comp = _ConcreteComponent()
        assert comp.normal_mode is False
        assert comp.is_visible is True
        assert isinstance(comp._renderer, GradientRenderer)
        assert comp.theme.name == "default"

    def test_creates_with_normal_mode_true(self) -> None:
        comp = _ConcreteComponent(normal_mode=True)
        assert comp.normal_mode is True
        assert comp._renderer.normal_mode is True

    def test_normal_mode_env_override(self) -> None:
        with patch.dict(os.environ, {"ECHOUI_NORMAL_MODE": "1"}):
            comp = _ConcreteComponent(normal_mode=False)
            assert comp.normal_mode is True

        with patch.dict(os.environ, {"ECHOUI_NORMAL_MODE": "true"}):
            comp = _ConcreteComponent(normal_mode=False)
            assert comp.normal_mode is True

        with patch.dict(os.environ, {"ECHOUI_NORMAL_MODE": "yes"}):
            comp = _ConcreteComponent(normal_mode=False)
            assert comp.normal_mode is True

        with patch.dict(os.environ, {"ECHOUI_NORMAL_MODE": "0"}):
            comp = _ConcreteComponent(normal_mode=False)
            assert comp.normal_mode is False

    def test_show_hide_toggle(self) -> None:
        comp = _ConcreteComponent()
        assert comp.is_visible is True
        comp.hide()
        assert comp.is_visible is False
        comp.show()
        assert comp.is_visible is True

    def test_repr_contains_class_name(self) -> None:
        comp = _ConcreteComponent(normal_mode=True)
        repr_str = repr(comp)
        assert "_ConcreteComponent" in repr_str
        assert "normal_mode=True" in repr_str
        assert "theme=" in repr_str

    def test_render_is_abstract(self) -> None:
        with pytest.raises(TypeError):
            _BrokenComponent()
