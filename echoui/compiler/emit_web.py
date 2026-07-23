"""Emit HTML and minimal JS runtime for web targets."""

from __future__ import annotations

import html
import json
from typing import Any, Dict

_BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,sans-serif;background:#fafafa;color:#1a1a1a}
.e-row{display:flex;flex-direction:row;gap:8px;align-items:stretch}
.e-col{display:flex;flex-direction:column;gap:8px}
.e-btn{padding:8px 16px;border:1px solid #ccc;border-radius:6px;background:#fff;cursor:pointer}
.e-btn:hover{background:#f0f0f0}
.e-screen{padding:24px;min-height:100vh}
.e-stage{position:relative;overflow:hidden}
.e-free{position:absolute}
"""

_RUNTIME_JS = """
(function(){
var S={},H={},B={};
function q(id){return document.getElementById(id);}
function bind(id,fn){B[id]=fn;}
function setText(id,t){var el=q(id);if(el)el.textContent=t;}
function onClick(id,fn){var el=q(id);if(el)el.addEventListener('click',fn);}
window.__echoui={bind:setText,onClick:onClick,handlers:H,signals:S};
document.addEventListener('DOMContentLoaded',function(){
  var cfg=window.__ECHoui_CFG||{};
  (cfg.clicks||[]).forEach(function(c){
    onClick(c.node,function(){fetch('/api/action',{method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({handler:c.handler})}).catch(function(){});
    });
  });
  (cfg.bindings||[]).forEach(function(b){
    if(b.type==='static')setText(b.node,b.value);
  });
});
})();
"""


def emit_web(lowered: Dict[str, Any], *, ssr_html: str | None = None) -> Dict[str, str]:
    body = ssr_html if ssr_html else _render_nodes(lowered["nodes"])
    clicks = [{"node": n["id"], "handler": hid} for n, hid in _click_entries(lowered)]
    bindings = _static_bindings(lowered["nodes"])
    cfg = json.dumps({"clicks": clicks, "bindings": bindings})
    page = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(lowered.get('app',{}).get('title','EchoUI'))}</title>
<style>{_BASE_CSS}</style>
</head><body>
<div id="app">{body}</div>
<script>window.__ECHoui_CFG={cfg};</script>
<script>{_RUNTIME_JS.strip()}</script>
</body></html>"""
    return {"index.html": page, "runtime.js": _RUNTIME_JS.strip()}


def _render_nodes(nodes: Dict[str, Any] | list[Dict[str, Any]]) -> str:
    if isinstance(nodes, list):
        return "".join(_render_node(n) for n in nodes)
    return _render_node(nodes)


def _render_node(node: Dict[str, Any]) -> str:
    tag = node.get("tag", "div")
    nid = node.get("id", "")
    props = node.get("props", {})
    cls = _class_for(node)
    attrs = f' id="{html.escape(nid)}" class="{html.escape(cls)}"'
    style_attr = _style_attr(props)
    if style_attr:
        attrs += f' style="{style_attr}"'
    if tag == "input":
        return f'<input{attrs} name="{html.escape(str(props.get("name","")))}"/>'
    if tag == "img":
        return f'<img{attrs} src="{html.escape(str(props.get("src","")))}" alt=""/>'
    if tag == "hr":
        return f"<hr{attrs}/>"
    inner = html.escape(_text_content(props))
    kids = "".join(_render_node(c) for c in node.get("children", []))
    return f"<{tag}{attrs}>{inner}{kids}</{tag}>"


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
    if "x" in props or "y" in props:
        parts.append("e-free")
    return " ".join(parts)


def _style_attr(props: Dict[str, Any]) -> str:
    bits: list[str] = []
    if "x" in props:
        bits.append(f"left:{props['x']}px")
    if "y" in props:
        bits.append(f"top:{props['y']}px")
    if "background" in props:
        bits.append(f"background:{props['background']}")
    if "width" in props and props.get("layout") == "free":
        bits.append(f"width:{props['width']}px")
    if "height" in props and props.get("layout") == "free":
        bits.append(f"height:{props['height']}px"
                    if isinstance(props["height"], (int, float))
                    else f"height:{props['height']}")
    if "transform" in props:
        bits.append(f"transform:{props['transform']}")
    return ";".join(bits)


def _walk(nodes: Dict[str, Any] | list[Dict[str, Any]]):
    if isinstance(nodes, dict):
        nodes = [nodes]
    for node in nodes:
        yield node
        for c in node.get("children", []):
            yield from _walk(c)


def _click_entries(lowered: Dict[str, Any]) -> list[tuple[Dict[str, Any], str]]:
    cmap = lowered.get("click_map", {})
    roots = lowered["nodes"]
    if isinstance(roots, dict):
        roots = [roots]
    out: list[tuple[Dict[str, Any], str]] = []
    for n in _walk(roots):
        hid = cmap.get(n["id"])
        if hid:
            out.append((n, hid))
    return out


def _text_content(props: Dict[str, Any]) -> str:
    text = props.get("text", props.get("label", ""))
    if callable(text):
        text = text()
    return str(text)


def _static_bindings(nodes: Dict[str, Any] | list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    if isinstance(nodes, dict):
        nodes = [nodes]
    out: list[Dict[str, Any]] = []
    for n in _walk(nodes):
        text = n.get("props", {}).get("text")
        if text is not None:
            if callable(text):
                text = text()
            out.append({"node": n["id"], "type": "static", "value": str(text)})
    return out
