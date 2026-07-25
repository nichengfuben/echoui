"""Compile Python click/key handlers to client-side JS at build time."""

from __future__ import annotations

import ast
import inspect
import textwrap
from typing import Any, Callable, Dict, List, Optional

from echoui.compiler.emit_frame import (
    _build_ctx,
    _compile_body,
    _emit_op,
    _lookup_callable,
    _resolve_frame_body,
)


def compile_handler(
    handler: Callable[..., Any], *, app_initial: str = "Home"
) -> Optional[Dict[str, Any]]:
    src = _handler_source(handler)
    if src is None:
        return None
    if src.lstrip().startswith("lambda"):
        expr = ast.parse(src, mode="eval").body
        if isinstance(expr, ast.Lambda):
            expr = expr.body
    else:
        tree = ast.parse(src)
        if not tree.body:
            return None
        stmt = tree.body[0]
        if isinstance(stmt, ast.FunctionDef):
            if not stmt.body:
                return None
            inner = stmt.body[0]
            if isinstance(inner, ast.Expr):
                expr = inner.value
            elif isinstance(inner, ast.Return) and inner.value:
                expr = inner.value
            else:
                return _compile_handler_body(handler)
        elif isinstance(stmt, ast.Expr):
            expr = stmt.value
        else:
            return None
    globs = getattr(handler, "__globals__", {})
    desc = _compile_expr(expr, globs, handler)
    if desc:
        return desc
    desc = _compile_nav_call(expr, globs, app_initial)
    if desc:
        return desc
    desc = _compile_call_action(expr, globs, handler)
    if desc:
        return desc
    return _compile_handler_body(handler)


def _compile_handler_body(handler: Callable[..., Any]) -> Optional[Dict[str, Any]]:
    """Compile full handler body (e.g. ``DashStore().value += 1``) to local JS."""
    body_fn = _resolve_frame_body(handler) or handler
    ctx = _build_ctx(body_fn)
    ops = _compile_body(body_fn, ctx)
    if not ops:
        return None
    return {"local": True, "script": _emit_action_js(ops)}


def _handler_source(handler: Callable[..., Any]) -> Optional[str]:
    injected = getattr(handler, "__echoui_source__", None)
    if isinstance(injected, str) and injected.strip():
        return injected
    try:
        lines, _ = inspect.getsourcelines(handler)
        src = textwrap.dedent("".join(lines)).strip()
    except (OSError, TypeError):
        return None
    if "lambda" not in src:
        return src
    idx = src.index("lambda")
    frag = src[idx:]
    colon = frag.find(":")
    if colon < 0:
        return src
    body = frag[colon + 1 :].lstrip()
    depth = 0
    for i, ch in enumerate(body):
        if ch == "(":
            depth += 1
        elif ch == ")":
            if depth == 0:
                return f"lambda: {body[:i].strip()}"
            depth -= 1
        elif ch == "," and depth == 0:
            return f"lambda: {body[:i].strip()}"
    trimmed = body.strip().rstrip("),")
    return f"lambda: {trimmed}"


def _compile_nav_call(
    node: ast.AST, globals_dict: dict[str, Any], app_initial: str
) -> Optional[Dict[str, Any]]:
    """Compile ``router.navigate('/path')`` to local page navigation."""
    if not isinstance(node, ast.Call):
        return None
    path: Optional[str] = None
    router: Any = None
    if isinstance(node.func, ast.Attribute) and node.func.attr == "navigate":
        if not node.args or not isinstance(node.args[0], ast.Constant):
            return None
        path = str(node.args[0].value)
        if isinstance(node.func.value, ast.Name):
            router = globals_dict.get(node.func.value.id)
    elif _name(node.func) == "navigate" and len(node.args) >= 2:
        if isinstance(node.args[0], ast.Name):
            router = globals_dict.get(node.args[0].id)
        if isinstance(node.args[1], ast.Constant):
            path = str(node.args[1].value)
    if router is None or path is None:
        return None
    from echoui.router import Router

    if not isinstance(router, Router):
        return None
    try:
        screen, _ = router.navigate(path)
    except LookupError:
        return None
    href = "index.html" if screen == app_initial else f"{screen.lower()}.html"
    return {"k": "nav", "path": path, "screen": screen, "href": href, "local": True}


def _compile_call_action(
    node: ast.AST, globals_dict: dict[str, Any], handler: Callable[..., Any]
) -> Optional[Dict[str, Any]]:
    """Resolve ``jump()`` / ``reset_game()``-style calls and compile to local JS."""
    if not isinstance(node, ast.Call):
        return None
    name = _name(node.func)
    if not name:
        return None
    fn = _lookup_callable(handler, name) or globals_dict.get(name)
    if not callable(fn):
        return None
    script = compile_action_script(fn)
    if script:
        return {"local": True, "script": script}
    return None


def compile_action_script(fn: Callable[..., Any]) -> Optional[str]:
    """Compile a module-level game/action function body to client JS."""
    body_fn = _resolve_frame_body(fn) or fn
    ctx = _build_ctx(body_fn)
    ops = _compile_body(body_fn, ctx)
    if not ops:
        return None
    return _emit_action_js(ops)


def _emit_action_js(ops: List[Dict[str, Any]]) -> str:
    lines = ["function g(k){return S[k];}"]
    for op in ops:
        lines.extend(_emit_op(op, 0))
    return "\n".join(lines)


def _compile_expr(
    node: ast.AST, globals_dict: dict[str, Any], handler: Callable[..., Any]
) -> Optional[Dict[str, Any]]:
    if isinstance(node, ast.Call) and _name(node.func) == "setattr":
        args = node.args
        if len(args) < 3:
            return None
        field = _const_str(args[1])
        if field is None:
            return None
        store_key = _resolve_store_class(args[0], globals_dict)
        if store_key is None:
            return None
        sig = f"{store_key}.{field}"
        val = args[2]
        if isinstance(val, ast.BinOp) and isinstance(val.op, ast.Add):
            if _is_store_field(val.left, store_key, field, globals_dict) and isinstance(
                val.right, ast.Constant
            ):
                return {"k": "inc", "s": sig, "by": val.right.value, "local": True}
        if isinstance(val, ast.BinOp) and isinstance(val.op, ast.Sub):
            if _is_store_field(val.left, store_key, field, globals_dict) and isinstance(
                val.right, ast.Constant
            ):
                return {"k": "dec", "s": sig, "by": val.right.value, "local": True}
        if isinstance(val, ast.Constant):
            return {"k": "set", "s": sig, "v": val.value, "local": True}
    return None


def _resolve_store_class(node: ast.AST, globals_dict: dict[str, Any]) -> Optional[str]:
    from echoui.state import Store

    if isinstance(node, ast.Name):
        obj = globals_dict.get(node.id)
        if isinstance(obj, Store):
            return obj.__class__.__name__
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
        obj = globals_dict.get(node.value.id)
        if isinstance(obj, Store):
            return obj.__class__.__name__
    return None


def _name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""


def _const_str(node: ast.AST) -> Optional[str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _is_store_field(
    node: ast.AST, class_name: str, field: str, globals_dict: dict[str, Any]
) -> bool:
    if isinstance(node, ast.Attribute) and node.attr == field:
        if isinstance(node.value, ast.Name):
            obj = globals_dict.get(node.value.id)
            from echoui.state import Store

            if isinstance(obj, Store):
                return obj.__class__.__name__ == class_name
    return False


def compile_actions(
    handlers: Dict[str, Callable[..., Any]], *, app_initial: str = "Home"
) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for hid, fn in handlers.items():
        desc = compile_handler(fn, app_initial=app_initial)
        if desc:
            out[hid] = desc
    return out
