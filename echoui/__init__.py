"""EchoUI public API surface."""

from typing import Any

from echoui.app import App
from echoui.clone import clone_pool
from echoui.events import on
from echoui.layout import (
    box,
    button,
    center,
    col,
    divider,
    grid,
    heading,
    image,
    input,
    input_field,
    link,
    paragraph,
    row,
    scroll,
    spacer,
    stack,
    text,
)
from echoui.raw import native_component
from echoui.reactive import computed
from echoui.screen import Screen
from echoui.signals import signal
from echoui.sprite import Sprite
from echoui.stage import Stage
from echoui.stage import stage as stage_fn
from echoui.state import Store
from echoui.style import css, keyframes_css, set_theme, style, theme

__version__ = "1.0.0"

# Built-in role factories — resolved via layout module
_BUILTIN_ROLE_NAMES = (
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
    "audio",
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
)

__all__ = [
    "App",
    "Screen",
    "Stage",
    "stage",
    "Sprite",
    "Store",
    "computed",
    "signal",
    "row",
    "col",
    "grid",
    "stack",
    "text",
    "heading",
    "paragraph",
    "button",
    "style",
    "css",
    "keyframes_css",
    "set_theme",
    "theme",
    "on",
    "native_component",
    "clone_pool",
    "input",
    "input_field",
    "box",
    "scroll",
    "image",
    "link",
    "center",
    "divider",
    "spacer",
    "__version__",
    *_BUILTIN_ROLE_NAMES,
]


def stage(*children: Any, **props: Any) -> Any:
    return stage_fn(*children, **props)


def __getattr__(name: str) -> Any:
    if name in _BUILTIN_ROLE_NAMES:
        from echoui import layout as layout_mod

        return getattr(layout_mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
