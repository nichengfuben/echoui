"""Emit HTML and client reactive runtime for web targets."""

from __future__ import annotations

import html
import json
from typing import Any, Dict

from echoui.compiler.client_cfg import build_client_cfg
from echoui.runtime import load_web_runtime

_BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden}
#app{width:100%;height:100%}
body{font-family:system-ui,sans-serif;background:#000;color:#1a1a1a}
.e-row{display:flex;flex-direction:row;gap:8px;align-items:stretch}
.e-col{display:flex;flex-direction:column;gap:8px}
.e-btn{padding:8px 16px;border:1px solid #ccc;border-radius:6px;background:#fff;cursor:pointer}
.e-btn:hover{background:#f0f0f0}
.e-screen{padding:24px;min-height:100vh}
.e-stage{position:relative;overflow:hidden}
.e-stage.e-fill{position:fixed;inset:0;width:100vw;height:100vh;touch-action:none}
.e-stage-inner{position:absolute;left:0;top:0;transform-origin:0 0}
.e-free{position:absolute}
.e-gpu{position:absolute;left:0;top:0;pointer-events:none;z-index:1}
.e-stage-inner .e-btn,.e-stage-inner .e-button,.e-stage-inner .e-free[class*="text"]{z-index:2;pointer-events:auto}
.e-gpu-hide{visibility:hidden}
.e-canvas{display:block}
.e-chart,.e-map,.e-gantt{display:block}
.e-overlay{position:fixed;inset:0;background:rgba(0,0,0,.45);display:none;align-items:center;justify-content:center;z-index:1000}
.e-overlay.e-overlay-open{display:flex}
.e-modal-panel,.e-drawer-panel,.e-sheet-panel{background:#fff;padding:20px;border-radius:8px;max-width:92vw;max-height:90vh;overflow:auto;box-shadow:0 8px 32px rgba(0,0,0,.2)}
.e-drawer-panel{position:fixed;top:0;bottom:0;width:min(420px,90vw)}
.e-drawer-panel.e-side-right{right:0}
.e-drawer-panel.e-side-left{left:0}
.e-file-input{margin:8px 0}
.e-img{object-fit:contain}
"""


def emit_web(lowered: Dict[str, Any], *, ssr_html: str | None = None) -> Dict[str, str]:
    gpu = lowered.get("free_gpu")
    body = ssr_html if ssr_html else _render_nodes(lowered["nodes"], gpu=gpu)
    cfg = json.dumps(build_client_cfg(lowered), ensure_ascii=False)
    runtime = load_web_runtime()
    title = html.escape(lowered.get("app", {}).get("title", "EchoUI"))
    page = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="manifest" href="manifest.webmanifest">
<style>{_BASE_CSS}</style>
</head><body>
<div id="app">{body}</div>
<script>window.__ECHoui_CFG={cfg};</script>
<script src="runtime.js"></script>
</body></html>"""
    return {"index.html": page, "runtime.js": runtime}


def _render_nodes(
    nodes: Dict[str, Any] | list[Dict[str, Any]], *, gpu: Dict[str, Any] | None = None
) -> str:
    if isinstance(nodes, list):
        return "".join(_render_node(n, gpu=gpu) for n in nodes)
    return _render_node(nodes, gpu=gpu)


def _render_node(node: Dict[str, Any], *, gpu: Dict[str, Any] | None = None) -> str:
    role = node.get("role", "box")
    props = node.get("props", {})
    if role == "raw":
        kind = props.get("kind", "")
        if kind == "js":
            return f"<script>{props.get('code', '')}</script>"
        if kind == "html":
            return str(props.get("content", ""))
        if kind == "css":
            return f"<style>{props.get('rules', '')}</style>"
    if role == "canvas":
        w = props.get("width", 800)
        h = props.get("height", 600)
        nid = node.get("id", "")
        script = _canvas_script(nid, node.get("canvas_commands", props.get("commands", [])))
        return f'<canvas id="{html.escape(nid)}" class="e-canvas" width="{w}" height="{h}"></canvas>{script}'
    if role == "chart":
        return _render_chart(node)
    if role == "map":
        return _render_map(node)
    if role == "gantt":
        return _render_gantt(node)
    if role == "stage":
        return _render_stage(node, gpu=gpu)
    if role == "screen":
        return _render_screen(node, gpu=gpu)
    overlay_role = props.get("role")
    if overlay_role in ("modal", "drawer", "sheet", "alert", "confirm"):
        return _render_overlay(node, gpu=gpu)
    tag = node.get("tag", "div")
    nid = node.get("id", "")
    cls = _class_for(node)
    attrs = f' id="{html.escape(nid)}" class="{html.escape(cls)}"'
    style_attr = _style_attr(props)
    if style_attr:
        attrs += f' style="{style_attr}"'
    if tag == "input":
        return _render_input(node, attrs)
    if tag == "img":
        alt = html.escape(str(props.get("alt", "")))
        src = html.escape(str(props.get("src", "")))
        return f'<img{attrs} class="{html.escape(cls)} e-img" src="{src}" alt="{alt}"/>'
    if tag == "video":
        src = html.escape(str(props.get("src", "")))
        return (
            f"<video{attrs} src=\"{src}\" controls playsinline "
            f'width="{props.get("width", 640)}" height="{props.get("height", 360)}"></video>'
        )
    if tag == "audio":
        src = html.escape(str(props.get("src", "")))
        return f"<audio{attrs} src=\"{src}\" controls></audio>"
    if tag == "hr":
        return f"<hr{attrs}/>"
    inner = html.escape(_text_content(props))
    kids = "".join(_render_node(c, gpu=gpu) for c in node.get("children", []))
    cls_extra = " e-gpu-hide" if gpu and _is_gpu_child(node, gpu) else ""
    if cls_extra:
        attrs = attrs.replace(f'class="{html.escape(cls)}"', f'class="{html.escape(cls + cls_extra)}"')
    return f"<{tag}{attrs}>{inner}{kids}</{tag}>"


def _render_input(node: Dict[str, Any], attrs: str) -> str:
    props = node.get("props", {})
    role = node.get("role", "input")
    name = html.escape(str(props.get("name", "")))
    itype = str(props.get("type", "text"))
    if role == "file_input":
        itype = "file"
    parts = [attrs, f'type="{html.escape(itype)}"', f'name="{name}"', 'class="e-file-input"']
    if itype == "file" and props.get("accept"):
        parts.append(f'accept="{html.escape(str(props["accept"]))}"')
    if props.get("placeholder"):
        parts.append(f'placeholder="{html.escape(str(props["placeholder"]))}"')
    if props.get("value") is not None:
        parts.append(f'value="{html.escape(str(props["value"]))}"')
    if props.get("checked"):
        parts.append("checked")
    if props.get("disabled"):
        parts.append("disabled")
    if props.get("min") is not None:
        parts.append(f'min="{html.escape(str(props["min"]))}"')
    if props.get("max") is not None:
        parts.append(f'max="{html.escape(str(props["max"]))}"')
    label = props.get("label")
    inp = f"<input {' '.join(parts)}/>"
    if label:
        return f'<label>{html.escape(str(label))}{inp}</label>'
    return inp


def _render_overlay(node: Dict[str, Any], *, gpu: Dict[str, Any] | None = None) -> str:
    props = node.get("props", {})
    kind = props.get("role", "modal")
    nid = node.get("id", "")
    open_sig = props.get("_open_signal", "")
    side = props.get("side", "right")
    panel_cls = f"e-{kind}-panel e-side-{side}" if kind == "drawer" else f"e-{kind}-panel"
    kids = "".join(_render_node(c, gpu=gpu) for c in node.get("children", []))
    msg = html.escape(str(props.get("message", "")))
    inner = kids or (f"<p>{msg}</p>" if msg else "")
    data_open = f' data-open-signal="{html.escape(open_sig)}"' if open_sig else ""
    return (
        f'<div id="{html.escape(nid)}" class="e-overlay e-{html.escape(kind)}" '
        f'aria-hidden="true"{data_open}>'
        f'<div class="{panel_cls}">{inner}</div></div>'
    )


def _is_gpu_child(node: Dict[str, Any], gpu: Dict[str, Any]) -> bool:
    return any(n.get("id") == node.get("id") for n in gpu.get("nodes", []))


def _render_screen(node: Dict[str, Any], *, gpu: Dict[str, Any] | None = None) -> str:
    props = node.get("props", {})
    children = node.get("children", [])
    if props.get("layout") == "free" and len(children) == 1 and children[0].get("role") == "stage":
        return _render_stage(children[0], gpu=gpu)
    nid = node.get("id", "")
    cls = _class_for(node)
    style_attr = _style_attr(props)
    attrs = f' id="{html.escape(nid)}" class="{html.escape(cls)}"'
    if style_attr:
        attrs += f' style="{style_attr}"'
    kids = "".join(_render_node(c, gpu=gpu) for c in children)
    return f"<div{attrs}>{kids}</div>"


def _render_stage(node: Dict[str, Any], *, gpu: Dict[str, Any] | None = None) -> str:
    props = node.get("props", {})
    nid = node.get("id", "")
    cls = _class_for(node)
    w = props.get("width", 640)
    h = props.get("height", 360)
    bg = props.get("background", "#101020")
    fill = props.get("fill_viewport", props.get("layout") == "free")
    gpu_canvas = ""
    if gpu and props.get("layout") == "free":
        cid = html.escape(gpu.get("canvas", f"gpu-{nid}"))
        gpu_canvas = f'<canvas id="{cid}" class="e-gpu e-canvas" width="{w}" height="{h}"></canvas>'
    kids = "".join(_render_node(c, gpu=gpu) for c in node.get("children", []))
    if fill:
        outer_cls = html.escape(f"{cls} e-fill")
        return (
            f'<div id="{html.escape(nid)}" class="{outer_cls}" '
            f'style="background:{bg}">'
            f'<div class="e-stage-inner" data-w="{w}" data-h="{h}" '
            f'style="width:{w}px;height:{h}px">'
            f"{gpu_canvas}{kids}</div></div>"
        )
    attrs = f' id="{html.escape(nid)}" class="{html.escape(cls)}" style="width:{w}px;height:{h}px;background:{bg}"'
    return f"<div{attrs}>{gpu_canvas}{kids}</div>"


def _render_chart(node: Dict[str, Any]) -> str:
    props = node.get("props", {})
    nid = node.get("id", "")
    w = int(props.get("width", 400))
    h = int(props.get("height", 240))
    data = props.get("data", props.get("series", [10, 24, 18, 32, 28]))
    if isinstance(data, dict):
        data = data.get("values", list(data.values()))
    values = list(data)
    production = props.get("production", True)
    if props.get("engine") == "canvas2d":
        production = False
    if production:
        payload = html.escape(json.dumps(values))
        chart_type = html.escape(str(props.get("type", "bar")))
        return (
            f'<canvas id="{html.escape(nid)}" class="e-chart e-chartjs e-canvas" '
            f'data-values="{payload}" data-chart-type="{chart_type}" '
            f'width="{w}" height="{h}"></canvas>'
        )
    n = max(len(values), 1)
    bw = max(8, w // n - 4)
    payload = json.dumps(values)
    script = (
        f"<script>(function(){{var c=document.getElementById('{nid}');if(!c)return;"
        f"var x=c.getContext('2d');var d={payload};var bw={bw};"
        f"x.fillStyle='#fafafa';x.fillRect(0,0,{w},{h});var maxV=Math.max.apply(null,d.concat([1]));"
        f"d.forEach(function(v,i){{x.fillStyle='#6200EE';var bh=Math.round((v/maxV)*({h}-30));"
        f"x.fillRect(20+i*(bw+8),{h}-bh-10,bw,bh);}});}})();</script>"
    )
    return f'<canvas id="{html.escape(nid)}" class="e-chart e-canvas" width="{w}" height="{h}"></canvas>{script}'


def _render_map(node: Dict[str, Any]) -> str:
    props = node.get("props", {})
    nid = node.get("id", "")
    w = int(props.get("width", 480))
    h = int(props.get("height", 320))
    lat = props.get("lat", 0)
    lng = props.get("lng", 0)
    zoom = props.get("zoom", 2)
    production = props.get("production", True)
    if props.get("engine") == "placeholder":
        production = False
    if production:
        return (
            f'<div id="{html.escape(nid)}" class="e-map e-maplibre" '
            f'data-lat="{lat}" data-lng="{lng}" data-zoom="{zoom}" '
            f'style="width:{w}px;height:{h}px"></div>'
        )
    return (
        f'<div id="{html.escape(nid)}" class="e-map" style="width:{w}px;height:{h}px;'
        f'background:linear-gradient(#aadaff,#dfeef9);position:relative;border:1px solid #ccc">'
        f'<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);'
        f'font:12px system-ui;color:#333">Map {lat},{lng} z{zoom}</div></div>'
    )


def _render_gantt(node: Dict[str, Any]) -> str:
    props = node.get("props", {})
    nid = node.get("id", "")
    tasks = props.get("tasks", props.get("rows", [{"name": "Task A", "start": 0, "end": 3}]))
    w = int(props.get("width", 520))
    h = int(props.get("height", max(120, 40 + len(tasks) * 28)))
    rows = ""
    for i, task in enumerate(tasks):
        name = html.escape(str(task.get("name", f"T{i+1}")))
        start = float(task.get("start", 0))
        end = float(task.get("end", start + 1))
        width = max(8, int((end - start) * 40))
        rows += (
            f'<div style="display:flex;align-items:center;height:24px;margin:2px 0">'
            f'<span style="width:110px;font:12px system-ui">{name}</span>'
            f'<div style="margin-left:8px;height:16px;width:{width}px;background:#2ecc71;border-radius:3px"></div></div>'
        )
    return (
        f'<div id="{html.escape(nid)}" class="e-gantt" style="width:{w}px;min-height:{h}px;'
        f'padding:8px;background:#fff;border:1px solid #ddd">{rows}</div>'
    )


def _canvas_script(nid: str, commands: list) -> str:
    if not commands:
        return ""
    payload = json.dumps(commands)
    return (
        f"<script>(function(){{var c=document.getElementById('{nid}');"
        f"if(!c)return;var x=c.getContext('2d');var cmds={payload};"
        "cmds.forEach(function(cmd){if(cmd.op==='clear'){x.fillStyle=cmd.color;x.fillRect(0,0,c.width,c.height);}"
        "else if(cmd.op==='fillRect'){x.fillStyle=cmd.color;x.fillRect(cmd.x,cmd.y,cmd.w,cmd.h);}"
        "else if(cmd.op==='text'){x.fillStyle=cmd.color;x.font=cmd.size+'px sans-serif';x.fillText(cmd.text,cmd.x,cmd.y);}});"
        "})();</script>"
    )


def _class_for(node: Dict[str, Any]) -> str:
    role = node.get("role", "box")
    props = node.get("props", {})
    parts = [f"e-{role}"]
    if props.get("direction") == "row":
        parts.append("e-row")
    elif props.get("direction") == "col":
        parts.append("e-col")
    if props.get("layout") == "free" or role == "stage":
        parts.append("e-stage")
    if props.get("layout") == "free" or role == "screen":
        parts.append("e-free")
    if "x" in props or "y" in props:
        parts.append("e-free")
    if props.get("class"):
        parts.append(str(props["class"]))
    if props.get("css_class"):
        parts.append(str(props["css_class"]))
    return " ".join(parts)


def _style_attr(props: Dict[str, Any]) -> str:
    bits: list[str] = []
    if "x" in props:
        bits.append(f"left:{_style_value(props['x'])}px")
    if "y" in props:
        bits.append(f"top:{_style_value(props['y'])}px")
    if "background" in props:
        bits.append(f"background:{props['background']}")
    if "width" in props:
        w = props["width"]
        bits.append(f"width:{w}px" if isinstance(w, (int, float)) else f"width:{w}")
    if "height" in props:
        h = props["height"]
        bits.append(
            f"height:{h}px"
            if isinstance(h, (int, float))
            else f"height:{h}"
        )
    if "opacity" in props:
        bits.append(f"opacity:{props['opacity']}")
    if "transform" in props:
        bits.append(f"transform:{props['transform']}")
    if props.get("hidden"):
        bits.append("display:none")
    return ";".join(bits)


def _walk(nodes: Dict[str, Any] | list[Dict[str, Any]]):
    if isinstance(nodes, dict):
        nodes = [nodes]
    for node in nodes:
        yield node
        for c in node.get("children", []):
            yield from _walk(c)


def _style_value(value: Any) -> Any:
    if callable(value):
        return value()
    return value


def _text_content(props: Dict[str, Any]) -> str:
    text = props.get("text", props.get("label", ""))
    if callable(text):
        text = text()
    return str(text)
