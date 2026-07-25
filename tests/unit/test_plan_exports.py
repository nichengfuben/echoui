"""PLAN.md export surface tests."""

import echoui
from echoui.plugin import api_binding, compiler_pass, role, target


def test_plan_core_exports():
    for name in ("App", "Screen", "Stage", "Sprite", "Store", "native_component"):
        assert hasattr(echoui, name)


def test_plan_role_exports():
    for name in ("chart", "map", "tabs", "calendar", "textarea", "switch"):
        assert hasattr(echoui, name)


def test_plugin_decorators_register():
    @role("test_role_x")
    def _render(sprite, target):
        return {}

    @compiler_pass("optimize")
    def _pass(ir):
        return ir

    @target("pdf")
    def _emit(ir):
        return ir

    @api_binding("payments")
    def _bind():
        return None

    assert _render is not None
    assert _pass is not None


def test_testing_a11y_audit_api():
    from echoui import App, Screen, button, col, text
    from echoui.testing import a11y_audit, mount

    class C(Screen):
        def build(self):
            return col(text("Hi"), button("Go", on_click=lambda: None))

    m = mount(App(screens=[C], initial="C"))
    report = a11y_audit(m)
    assert report.passes
