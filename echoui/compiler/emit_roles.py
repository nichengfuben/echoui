"""Production HTML emitters for all built-in roles."""

from __future__ import annotations

import html
import json
from typing import Any, Dict, Optional

_INPUT_TYPES: Dict[str, str] = {
    "input": "text",
    "password": "password",
    "number_input": "number",
    "checkbox": "checkbox",
    "radio": "radio",
    "slider": "range",
    "range_slider": "range",
    "switch": "checkbox",
    "color_picker": "color",
    "date_picker": "date",
    "time_picker": "time",
    "datetime_picker": "datetime-local",
    "file_input": "file",
    "combobox": "text",
}


def render_role_html(
    node: Dict[str, Any],
    *,
    attrs: str,
    cls: str,
    style_attr: str,
    inner: str,
    kids: str,
    gpu_hide: str = "",
) -> Optional[str]:
    """Return full HTML for node, or None to fall through to generic tag render."""
    role = node.get("role", "box")
    props = node.get("props", {})
    tag = node.get("tag", "div")
    nid = node.get("id", "")

    if role in _INPUT_TYPES or tag == "input":
        return _render_input(node, attrs, cls, style_attr)
    if role == "textarea" or tag == "textarea":
        return _render_textarea(node, attrs, cls, style_attr, inner)
    if role in ("select", "multiselect") or tag == "select":
        return _render_select(node, attrs, cls, style_attr, props)
    if role == "progress":
        val = props.get("value", 0)
        mx = props.get("max", 100)
        return f'<progress{attrs} class="{html.escape(cls)}" value="{val}" max="{mx}"{style_attr}></progress>'
    if role == "link" or tag == "a":
        href = html.escape(str(props.get("href", "#")))
        return f'<a{attrs} class="{html.escape(cls)}" href="{href}"{style_attr}>{inner}{kids}</a>'
    if role == "badge":
        return f'<span{attrs} class="{html.escape(cls)} e-badge"{style_attr}>{inner or html.escape(str(props.get("text", "")))}</span>'
    if role == "avatar":
        src = html.escape(str(props.get("src", "")))
        alt = html.escape(str(props.get("alt", "avatar")))
        if src:
            return f'<img{attrs} class="{html.escape(cls)} e-avatar" src="{src}" alt="{alt}"{style_attr}/>'
        label = html.escape(str(props.get("label", props.get("text", "A"))[:1]))
        return f'<span{attrs} class="{html.escape(cls)} e-avatar e-avatar-fallback"{style_attr}>{label}</span>'
    if role == "chip":
        return f'<span{attrs} class="{html.escape(cls)} e-chip"{style_attr}>{inner or html.escape(str(props.get("text", "")))}</span>'
    if role == "spinner":
        return f'<span{attrs} class="{html.escape(cls)} e-spinner" aria-busy="true"{style_attr}></span>'
    if role == "skeleton":
        w = props.get("width", 120)
        h = props.get("height", 16)
        return f'<span{attrs} class="{html.escape(cls)} e-skeleton" style="display:inline-block;width:{w}px;height:{h}px"{style_attr}></span>'
    if role == "divider" or tag == "hr":
        return f"<hr{attrs} class=\"{html.escape(cls)}\"{style_attr}/>"
    if role == "spacer":
        sz = props.get("size", 8)
        return f'<div{attrs} class="{html.escape(cls)} e-spacer" style="height:{sz}px"{style_attr}></div>'
    if role == "scroll":
        mh = props.get("max_height", 400)
        st = f";max-height:{mh}px;overflow:auto" if style_attr else f' style="max-height:{mh}px;overflow:auto"'
        if style_attr:
            st = style_attr.rstrip('"') + f";max-height:{mh}px;overflow:auto\""
        return f'<div{attrs} class="{html.escape(cls)} e-scroll"{st}>{kids or inner}</div>'
    if role == "card":
        return f'<article{attrs} class="{html.escape(cls)} e-card"{style_attr}>{kids or inner}</article>'
    if role == "table":
        return _render_table(node, attrs, cls, style_attr, props, kids)
    if role == "list_view" or role == "tree":
        return f'<ul{attrs} class="{html.escape(cls)} e-list"{style_attr}>{kids or inner}</ul>'
    if role == "tabs":
        return f'<div{attrs} class="{html.escape(cls)} e-tabs" role="tablist"{style_attr}>{kids}</div>'
    if role == "accordion":
        return f'<div{attrs} class="{html.escape(cls)} e-accordion"{style_attr}>{kids}</div>'
    if role == "breadcrumb":
        return f'<nav{attrs} class="{html.escape(cls)} e-breadcrumb" aria-label="breadcrumb"{style_attr}>{kids or inner}</nav>'
    if role == "pagination":
        return f'<nav{attrs} class="{html.escape(cls)} e-pagination"{style_attr}>{kids or inner}</nav>'
    if role == "code" or tag == "pre":
        code = html.escape(str(props.get("text", inner)))
        return f'<pre{attrs} class="{html.escape(cls)} e-code"{style_attr}><code>{code}</code></pre>'
    if role in ("richtext", "markdown"):
        return f'<div{attrs} class="{html.escape(cls)} e-richtext"{style_attr}>{inner}{kids}</div>'
    if role == "rating":
        stars = int(props.get("value", 0))
        mx = int(props.get("max", 5))
        sym = "★" * stars + "☆" * max(0, mx - stars)
        return f'<div{attrs} class="{html.escape(cls)} e-rating" aria-label="rating"{style_attr}>{sym}</div>'
    if role == "calendar":
        return f'<div{attrs} class="{html.escape(cls)} e-calendar"{style_attr}>{kids or inner or "Calendar"}</div>'
    if role == "carousel":
        return f'<div{attrs} class="{html.escape(cls)} e-carousel"{style_attr}>{kids}</div>'
    if role == "kanban":
        return f'<div{attrs} class="{html.escape(cls)} e-kanban"{style_attr}>{kids}</div>'
    if role == "splitter":
        return f'<div{attrs} class="{html.escape(cls)} e-splitter"{style_attr}>{kids}</div>'
    if role == "iframe" or role == "embed":
        src = html.escape(str(props.get("src", "")))
        return f'<iframe{attrs} class="{html.escape(cls)} e-embed" src="{src}"{style_attr}></iframe>'
    if role == "viewport3d":
        w = props.get("width", 640)
        h = props.get("height", 360)
        return f'<canvas{attrs} class="{html.escape(cls)} e-viewport3d" width="{w}" height="{h}"{style_attr}></canvas>'
    if role == "qr" or role == "barcode":
        w = props.get("width", 128)
        h = props.get("height", 128)
        data = html.escape(str(props.get("data", props.get("text", ""))))
        return (
            f'<canvas{attrs} class="{html.escape(cls)} e-{role}" width="{w}" height="{h}" '
            f'data-value="{data}"{style_attr}></canvas>'
        )
    if role == "virtual_list":
        item_h = props.get("item_height", 40)
        total = props.get("total", len(props.get("items", [])))
        height = props.get("height", 400)
        return (
            f'<div{attrs} class="{html.escape(cls)} e-virtual-list" '
            f'data-item-height="{item_h}" data-total="{total}" '
            f'style="height:{height}px;overflow:auto;position:relative"{style_attr.lstrip()}>'
            f'<div class="e-virtual-spacer" style="height:{item_h * total}px"></div>'
            f'<div class="e-virtual-viewport">{kids or inner}</div></div>'
        )
    if role == "stepper":
        step = props.get("step", 0)
        return f'<div{attrs} class="{html.escape(cls)} e-stepper" data-step="{step}"{style_attr}>{kids}</div>'
    if role == "tooltip":
        tip = html.escape(str(props.get("text", props.get("label", ""))))
        return f'<span{attrs} class="{html.escape(cls)} e-tooltip" title="{tip}"{style_attr}>{inner or kids}</span>'
    if role == "popover":
        return f'<div{attrs} class="{html.escape(cls)} e-popover"{style_attr}>{kids or inner}</div>'
    if role == "icon" or role == "svg":
        sym = html.escape(str(props.get("name", props.get("text", "●"))))
        return f'<span{attrs} class="{html.escape(cls)} e-icon" aria-hidden="true"{style_attr}>{sym}</span>'
    if role == "icon_button":
        sym = html.escape(str(props.get("icon", props.get("text", "●"))))
        lbl = html.escape(str(props.get("label", props.get("aria_label", "Button"))))
        return f'<button{attrs} class="{html.escape(cls)} e-btn e-icon-btn" aria-label="{lbl}"{style_attr}>{sym}</button>'
    if role == "radio_group":
        name = html.escape(str(props.get("name", "")))
        opts = props.get("options", [])
        items = ""
        for opt in opts:
            val = html.escape(str(opt.get("value", opt) if isinstance(opt, dict) else opt))
            lab = html.escape(str(opt.get("label", val) if isinstance(opt, dict) else opt))
            chk = " checked" if isinstance(opt, dict) and opt.get("selected") else ""
            items += f'<label class="e-radio"><input type="radio" name="{name}" value="{val}"{chk}/>{lab}</label>'
        return f'<fieldset{attrs} class="{html.escape(cls)} e-radio-group"{style_attr}>{items}</fieldset>'
    if role == "grid_view" or role == "collection":
        cols = props.get("cols", 3)
        gap = props.get("gap", 8)
        grid = f"display:grid;grid-template-columns:repeat({cols},1fr);gap:{gap}px"
        combined = f' style="{grid}"' if not style_attr else style_attr.rstrip('"') + f";{grid}\""
        return f'<div{attrs} class="{html.escape(cls)} e-grid-view"{combined}>{kids}</div>'
    if role in ("menu", "context_menu"):
        return f'<menu{attrs} class="{html.escape(cls)} e-menu"{style_attr}>{kids or inner}</menu>'
    if role == "menubar":
        return f'<nav{attrs} class="{html.escape(cls)} e-menubar" role="menubar"{style_attr}>{kids}</nav>'
    if role in ("resizable", "sortable"):
        return f'<div{attrs} class="{html.escape(cls)} e-{role}" data-resizable="true"{style_attr}>{kids}</div>'
    if role == "window":
        title = html.escape(str(props.get("title", "Window")))
        return f'<section{attrs} class="{html.escape(cls)} e-window"{style_attr}><header class="e-window-title">{title}</header>{kids}</section>'
    if role == "tray":
        return f'<aside{attrs} class="{html.escape(cls)} e-tray"{style_attr}>{kids or inner}</aside>'
    if role == "gantt":
        w = props.get("width", 800)
        h = props.get("height", 300)
        return f'<canvas{attrs} class="{html.escape(cls)} e-gantt" width="{w}" height="{h}"{style_attr}></canvas>'
    if role == "sprite":
        return f'<div{attrs} class="{html.escape(cls)} e-sprite"{style_attr}>{kids or inner}</div>'
    if role == "heading":
        level = min(6, max(1, int(props.get("level", 1))))
        return f'<h{level}{attrs} class="{html.escape(cls)}"{style_attr}>{inner or html.escape(str(props.get("text", "")))}</h{level}>'
    if role == "paragraph":
        return f'<p{attrs} class="{html.escape(cls)}"{style_attr}>{inner or html.escape(str(props.get("text", "")))}</p>'
    if role == "text":
        return f'<span{attrs} class="{html.escape(cls)}{gpu_hide}"{style_attr}>{inner or html.escape(str(props.get("text", "")))}</span>'
    if role == "button" or tag == "button":
        lbl = html.escape(str(props.get("label", props.get("text", "Button"))))
        return f'<button{attrs} class="{html.escape(cls)} e-btn"{style_attr}>{lbl}{kids}</button>'
    if props.get("display") == "grid":
        cols = props.get("cols", 2)
        gap = props.get("gap", 8)
        grid_style = f"display:grid;grid-template-columns:repeat({cols},1fr);gap:{gap}px"
        combined = f' style="{grid_style}"' if not style_attr else style_attr.rstrip('"') + f";{grid_style}\""
        return f'<div{attrs} class="{html.escape(cls)} e-grid"{combined}>{kids}</div>'
    if props.get("direction") == "row":
        gap = props.get("gap", 8)
        flex = f"display:flex;flex-direction:row;gap:{gap}px;align-items:{props.get('align','stretch')}"
        combined = f' style="{flex}"' if not style_attr else style_attr.rstrip('"') + f";{flex}\""
        return f'<div{attrs} class="{html.escape(cls)} e-row"{combined}>{kids}</div>'
    if props.get("direction") == "col":
        gap = props.get("gap", 8)
        flex = f"display:flex;flex-direction:column;gap:{gap}px"
        combined = f' style="{flex}"' if not style_attr else style_attr.rstrip('"') + f";{flex}\""
        return f'<div{attrs} class="{html.escape(cls)} e-col"{combined}>{kids}</div>'
    return None


def _render_input(node: Dict[str, Any], attrs: str, cls: str, style_attr: str) -> str:
    props = node.get("props", {})
    role = node.get("role", "input")
    itype = _INPUT_TYPES.get(role, str(props.get("type", "text")))
    name = html.escape(str(props.get("name", "")))
    parts = [attrs, f'type="{html.escape(itype)}"', f'name="{name}"', f'class="{html.escape(cls)} e-input"']
    if style_attr:
        parts.append(style_attr.lstrip())
    if itype == "file" and props.get("accept"):
        parts.append(f'accept="{html.escape(str(props["accept"]))}"')
    for key in ("placeholder", "value", "min", "max", "step"):
        if props.get(key) is not None:
            parts.append(f'{key}="{html.escape(str(props[key]))}"')
    if props.get("checked") or (role == "switch" and props.get("value")):
        parts.append("checked")
    if props.get("disabled"):
        parts.append("disabled")
    if role == "switch":
        parts.append('role="switch"')
    inp = f"<input {' '.join(parts)}/>"
    label = props.get("label")
    if label:
        return f'<label class="e-field">{html.escape(str(label))}{inp}</label>'
    return inp


def _render_textarea(node: Dict[str, Any], attrs: str, cls: str, style_attr: str, inner: str) -> str:
    props = node.get("props", {})
    name = html.escape(str(props.get("name", "")))
    rows = props.get("rows", 4)
    text = inner or html.escape(str(props.get("text", props.get("value", ""))))
    return (
        f'<textarea{attrs} class="{html.escape(cls)} e-textarea" name="{name}" '
        f'rows="{rows}"{style_attr}>{text}</textarea>'
    )


def _render_select(node: Dict[str, Any], attrs: str, cls: str, style_attr: str, props: Dict[str, Any]) -> str:
    name = html.escape(str(props.get("name", "")))
    multi = ' multiple' if node.get("role") == "multiselect" else ""
    options = props.get("options", [])
    opts_html = ""
    for opt in options:
        if isinstance(opt, dict):
            val = html.escape(str(opt.get("value", "")))
            lab = html.escape(str(opt.get("label", val)))
            sel = " selected" if opt.get("selected") else ""
        else:
            val = lab = html.escape(str(opt))
            sel = ""
        opts_html += f'<option value="{val}"{sel}>{lab}</option>'
    return f'<select{attrs} class="{html.escape(cls)} e-select" name="{name}"{multi}{style_attr}>{opts_html}</select>'


def _render_table(
    node: Dict[str, Any], attrs: str, cls: str, style_attr: str, props: Dict[str, Any], kids: str
) -> str:
    columns = props.get("columns", [])
    rows = props.get("rows", [])
    head = "".join(f"<th>{html.escape(str(c.get('label', c) if isinstance(c, dict) else c))}</th>" for c in columns)
    body = ""
    for row in rows:
        if isinstance(row, dict):
            cells = "".join(
                f"<td>{html.escape(str(row.get(c.get('key', c) if isinstance(c, dict) else c, '')))}</td>"
                for c in columns
            )
        else:
            cells = f"<td>{html.escape(str(row))}</td>"
        body += f"<tr>{cells}</tr>"
    return (
        f'<table{attrs} class="{html.escape(cls)} e-table"{style_attr}>'
        f"<thead><tr>{head}</tr></thead><tbody>{body or kids}</tbody></table>"
    )
