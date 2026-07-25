"""Accessibility audit tests."""

from echoui import App, Screen, button, col, text
from echoui.a11y import a11y_audit, labelled
from echoui.compiler.parser import parse_app
from echoui.layout import image


class Ok(Screen):
    def build(self):
        return col(
            text("Title"),
            button("OK", on_click=lambda: None),
        )


class BadImage(Screen):
    def build(self):
        node = image("logo.png")
        return col(labelled(node, "Logo"))


def test_a11y_audit_flags_unlabeled_image():
    app = App(screens=[BadImage], initial="BadImage")
    root = parse_app(app)["root"]
    issues = a11y_audit(root)
    assert any("missing alt" in issue for issue in issues)


def test_a11y_audit_ok_screen():
    app = App(screens=[Ok], initial="Ok")
    root = parse_app(app)["root"]
    assert a11y_audit(root) == []
