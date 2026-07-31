"""Role name to native tag registry."""

from __future__ import annotations

from typing import Any, Callable, Dict

ROLE_MAP: Dict[str, str] = {
    "text": "span",
    "heading": "h1",
    "paragraph": "p",
    "richtext": "div",
    "markdown": "div",
    "code": "pre",
    "button": "button",
    "icon_button": "button",
    "image": "img",
    "icon": "span",
    "svg": "svg",
    "input": "input",
    "textarea": "textarea",
    "password": "input",
    "number_input": "input",
    "checkbox": "input",
    "radio": "input",
    "radio_group": "div",
    "select": "select",
    "multiselect": "select",
    "combobox": "input",
    "slider": "input",
    "range_slider": "input",
    "switch": "input",
    "color_picker": "input",
    "date_picker": "input",
    "time_picker": "input",
    "datetime_picker": "input",
    "file_input": "input",
    "drop_target": "div",
    "box": "div",
    "card": "div",
    "scroll": "div",
    "spacer": "div",
    "divider": "hr",
    "link": "a",
    "video": "video",
    "audio_player": "audio",
    "canvas": "canvas",
    "viewport3d": "canvas",
    "embed": "iframe",
    "iframe": "iframe",
    "list_view": "ul",
    "table": "table",
    "tree": "ul",
    "grid_view": "div",
    "collection": "div",
    "virtual_list": "div",
    "tabs": "div",
    "accordion": "div",
    "stepper": "div",
    "breadcrumb": "nav",
    "pagination": "nav",
    "badge": "span",
    "avatar": "span",
    "chip": "span",
    "tooltip": "span",
    "popover": "div",
    "menu": "menu",
    "menubar": "nav",
    "context_menu": "menu",
    "progress": "progress",
    "spinner": "span",
    "skeleton": "span",
    "rating": "div",
    "calendar": "div",
    "gantt": "div",
    "kanban": "div",
    "carousel": "div",
    "splitter": "div",
    "resizable": "div",
    "sortable": "div",
    "chart": "canvas",
    "map": "div",
    "qr": "canvas",
    "barcode": "canvas",
    "window": "div",
    "tray": "div",
    "sprite": "div",
    "screen": "div",
    "stage": "div",
    "native": "div",
    "raw": "script",
}

_custom_roles: Dict[str, Callable[..., Any]] = {}


def register_role(name: str, tag: str) -> None:
    ROLE_MAP[name] = tag


def role_tag(role: str) -> str:
    return ROLE_MAP.get(role, "div")


def register_role_renderer(name: str, renderer: Callable[..., Any]) -> None:
    _custom_roles[name] = renderer
