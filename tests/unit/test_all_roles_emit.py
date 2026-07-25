"""Emit tests for all built-in roles."""

from __future__ import annotations

from echoui.compiler.emit_roles import render_role_html
from echoui.compiler.emit_web import _render_node
from echoui.roles import ROLE_MAP


def _emit_role(role: str, **props) -> str:
    node = {"id": f"n_{role}", "role": role, "tag": ROLE_MAP.get(role, "div"), "props": props, "children": []}
    via_roles = render_role_html(
        node,
        attrs=' id="n"',
        cls=f"e-{role}",
        style_attr="",
        inner="",
        kids="",
    )
    if via_roles:
        return via_roles
    return _render_node(node)


def test_all_roles_emit_non_empty():
    skip = {"screen", "stage", "native", "raw", "canvas", "chart", "map", "gantt"}
    missing = []
    for role in ROLE_MAP:
        if role in skip:
            continue
        html = _emit_role(role, text="x", label="L", name="f", options=[{"value": "a", "label": "A"}])
        if not html:
            missing.append(role)
    assert not missing, f"roles without emit: {missing}"


def test_virtual_list_emits_viewport():
    html = _emit_role("virtual_list", total=100, item_height=40, height=400)
    assert "e-virtual-list" in html
    assert "e-virtual-viewport" in html


def test_file_input_emits_accept():
    html = _emit_role("file_input", name="photo", accept="image/*", label="Photo")
    assert 'type="file"' in html
    assert "image/*" in html


def test_table_emits_rows():
    html = _emit_role("table", columns=[{"key": "name", "label": "Name"}], rows=[{"name": "Alice"}])
    assert "<table" in html
    assert "Alice" in html
