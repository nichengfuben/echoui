"""Flow layout helpers and role factories."""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Union

from echoui.sprite import IRNode, normalize_children


def row(*children: Any, gap: int = 8, align: str = "stretch", justify: str = "start", **extra: Any) -> IRNode:
    props = {"gap": gap, "align": align, "justify": justify, "direction": "row", **extra}
    return IRNode("box", props=props, children=normalize_children(list(children)))


def col(*children: Any, gap: int = 8, align: str = "stretch", **extra: Any) -> IRNode:
    props = {"gap": gap, "align": align, "direction": "col", **extra}
    return IRNode("box", props=props, children=normalize_children(list(children)))


def grid(*children: Any, cols: int = 2, gap: int = 8, **extra: Any) -> IRNode:
    props = {"cols": cols, "gap": gap, "display": "grid", **extra}
    return IRNode("box", props=props, children=normalize_children(list(children)))


def stack(*children: Any, **extra: Any) -> IRNode:
    return IRNode("box", props={"display": "stack", **extra}, children=normalize_children(list(children)))


def spacer(size: int = 8) -> IRNode:
    return IRNode("spacer", props={"size": size})


def divider() -> IRNode:
    return IRNode("divider")


def center(child: Any) -> IRNode:
    return IRNode("box", props={"align": "center", "justify": "center"}, children=normalize_children([child]))


def scroll(child: Any, max_height: int = 400) -> IRNode:
    return IRNode("scroll", props={"max_height": max_height}, children=normalize_children([child]))


def _role(
    role: str,
    *children: Any,
    text: Union[str, Callable[[], str], None] = None,
    label: Optional[str] = None,
    on_click: Optional[Callable[..., None]] = None,
    **props: Any,
) -> IRNode:
    p = dict(props)
    if text is not None:
        p["text"] = text
    if label is not None:
        p["label"] = label
    events: Dict[str, str] = {}
    if on_click is not None:
        events["click"] = on_click.__name__ if hasattr(on_click, "__name__") else "on_click"
        p["_handler_click"] = on_click
    bindings: Dict[str, Any] = {}
    if callable(text):
        p["_text_fn"] = text
        bindings["text"] = text
    return IRNode(
        role,
        props=p,
        children=normalize_children(list(children)) if children else [],
        events=events,
        bindings=bindings,
    )


def text(content: Union[str, Callable[[], str]], **props: Any) -> IRNode:
    return _role("text", text=content, **props)


def heading(content: Union[str, Callable[[], str]], level: int = 1, **props: Any) -> IRNode:
    return _role("heading", text=content, level=level, **props)


def paragraph(content: Union[str, Callable[[], str]], **props: Any) -> IRNode:
    return _role("paragraph", text=content, **props)


def button(label: str, on_click: Optional[Callable[..., None]] = None, **props: Any) -> IRNode:
    return _role("button", text=label, label=label, on_click=on_click, **props)


def image(src: str, alt: str = "", **props: Any) -> IRNode:
    return _role("image", src=src, alt=alt, **props)


def box(*children: Any, **props: Any) -> IRNode:
    return IRNode("box", props=props, children=normalize_children(list(children)))


def input_field(name: str, label: Optional[str] = None, **props: Any) -> IRNode:
    return _role("input", name=name, label=label or name, **props)


def link(href: str, label: str, **props: Any) -> IRNode:
    return _role("link", href=href, text=label, **props)


def _factory(role: str) -> Callable[..., IRNode]:
    def maker(*children: Any, **props: Any) -> IRNode:
        return _role(role, *children, **props)

    maker.__name__ = role
    return maker


# Built-in roles (each maps to a Sprite role; backends lower per target matrix)
_BUILTIN_ROLES = (
    "richtext",
    "markdown",
    "code",
    "icon_button",
    "icon",
    "svg",
    "textarea",
    "password",
    "number_input",
    "checkbox",
    "radio",
    "radio_group",
    "select",
    "multiselect",
    "combobox",
    "slider",
    "range_slider",
    "switch",
    "color_picker",
    "date_picker",
    "time_picker",
    "datetime_picker",
    "file_input",
    "card",
    "video",
    "audio_player",
    "canvas",
    "viewport3d",
    "embed",
    "iframe",
    "list_view",
    "table",
    "tree",
    "grid_view",
    "tabs",
    "accordion",
    "stepper",
    "breadcrumb",
    "pagination",
    "badge",
    "avatar",
    "chip",
    "tooltip",
    "popover",
    "menu",
    "menubar",
    "context_menu",
    "progress",
    "spinner",
    "skeleton",
    "rating",
    "calendar",
    "gantt",
    "kanban",
    "carousel",
    "splitter",
    "resizable",
    "sortable",
    "chart",
    "map",
    "qr",
    "barcode",
    "collection",
    "window",
    "tray",
    "sprite",
)

for _role_name in _BUILTIN_ROLES:
    globals()[_role_name] = _factory(_role_name)

# Aliases for common role naming (after factories exist)
input = input_field
audio = globals()["audio_player"]
