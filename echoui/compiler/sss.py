"""SSS tree validation and normalization.

App → Screen → Stage (free mode) → Sprite
App → Screen → Sprite (flow mode; col/row/box are Sprites)

Free-mode Screens must return ``stage(...)`` directly — never ``col(stage(), ...)``.
"""

from __future__ import annotations

from typing import Any, List

from echoui.exceptions import SSSError


def normalize_screen_tree(root: Any) -> Any:
    """Apply SSS rules to the compiled screen IR root."""
    layout = root.props.get("layout", "flow")
    if layout != "free":
        return root
    if len(root.children) != 1:
        _raise_free_screen(root)
    child = root.children[0]
    if child.role != "stage":
        _raise_free_screen(root, child)
    _apply_free_stage_defaults(child, background=root.props.get("background"))
    return root


def validate_sss_tree(root: Any) -> None:
    """Raise SSSError if the screen tree violates SSS rules."""
    normalize_screen_tree(root)
    layout = root.props.get("layout", "flow")
    if layout == "free":
        stage = root.children[0]
        _walk_stage_sprites(stage)


def _apply_free_stage_defaults(stage: Any, *, background: str = "") -> None:
    props = stage.props
    props.setdefault("layout", "free")
    props.setdefault("fill_viewport", True)
    if background:
        props.setdefault("background", background)


def _walk_stage_sprites(stage: Any) -> None:
    for child in stage.children:
        if child.role == "stage" and child.props.get("layout") == "free":
            raise SSSError("Stage must not nest another free Stage; use Sprite children.")


def _raise_free_screen(root: Any, bad: Any | None = None) -> None:
    if bad is not None and bad.role == "box":
        direction = bad.props.get("direction")
        if direction in ("col", "row") or _contains_stage(bad):
            raise SSSError(
                "free Screen.build() must return stage(...) directly. "
                "Do not wrap the Stage in col/row/box. "
                "Put HUD text, buttons, and game Sprites inside stage(...)."
            )
    if bad is not None and bad.role == "stage" and len(root.children) > 1:
        raise SSSError(
            "free Screen.build() must return a single stage(...). "
            "Extra siblings belong inside the Stage as Sprites."
        )
    raise SSSError(
        "free Screen.build() must return stage(...) as the root."
    )


def _contains_stage(node: Any) -> bool:
    if node.role == "stage":
        return True
    return any(_contains_stage(c) for c in node.children)


def free_screen_must_return_stage(children: List[Any]) -> List[Any]:
    """Normalize build() output for layout='free' Screen classes."""
    if not children:
        raise SSSError("free Screen.build() must return stage(...)")
    if len(children) == 1 and children[0].role == "stage":
        return children
    bad = children[0] if children else None
    fake = type("_Root", (), {"children": children, "props": {"layout": "free"}})()
    _raise_free_screen(fake, bad)
    return children  # unreachable
