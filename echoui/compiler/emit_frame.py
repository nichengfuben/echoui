"""Compile @on('frame') handlers to client-side JS for static builds."""

from __future__ import annotations

import ast
import inspect
import textwrap
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class FrameCtx:
    fn: Callable[..., Any]
    aliases: Dict[str, str] = field(default_factory=dict)
    consts: Dict[str, Any] = field(default_factory=dict)

    def store_class(self, var: str) -> Optional[str]:
        if var in self.aliases:
            return self.aliases[var]
        return _resolve_store_name(var, self.fn)

    def store_sig(self, node: ast.AST) -> Optional[str]:
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            cls = self.store_class(node.value.id)
            if cls:
                return f"{cls}.{node.attr}"
        return None


def compile_frame_script(
    frame_handlers: List[Dict[str, Any]], handlers: Dict[str, Callable[..., Any]]
) -> Optional[str]:
    if not frame_handlers:
        return None
    hid = frame_handlers[0]["handler"]
    fn = handlers.get(hid)
    if fn is None:
        return None
    body_fn = _resolve_frame_body(fn) or fn
    ctx = _build_ctx(body_fn)
    ops = _compile_body(body_fn, ctx)
    if not ops:
        return None
    return _emit_js(ops)


def _build_ctx(fn: Callable[..., Any]) -> FrameCtx:
    ctx = FrameCtx(fn=fn)
    mod = inspect.getmodule(fn)
    if mod:
        for name, val in vars(mod).items():
            if name.isupper() and isinstance(val, (int, float, bool)):
                ctx.consts[name] = val
    src = _fn_source(fn)
    if src:
        tree = ast.parse(src)
        if tree.body and isinstance(tree.body[0], ast.FunctionDef):
            for stmt in tree.body[0].body:
                if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
                    tgt = stmt.targets[0]
                    if isinstance(tgt, ast.Name) and isinstance(stmt.value, ast.Call):
                        cls = _call_store_class(stmt.value)
                        if cls:
                            ctx.aliases[tgt.id] = cls
    return ctx


def _call_store_class(node: ast.Call) -> Optional[str]:
    if isinstance(node.func, ast.Name) and node.func.id.endswith("Store"):
        return node.func.id
    return None


def _resolve_frame_body(fn: Callable[..., Any]) -> Optional[Callable[..., Any]]:
    src = _fn_source(fn)
    if src is None:
        return None
    tree = ast.parse(src)
    if not tree.body or not isinstance(tree.body[0], ast.FunctionDef):
        return None
    body = tree.body[0].body
    if len(body) == 1 and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Call):
        call = body[0].value
        if isinstance(call.func, ast.Name):
            return _lookup_callable(fn, call.func.id)
        if isinstance(call.func, ast.Attribute) and isinstance(call.func.value, ast.Name):
            return _lookup_callable(fn, call.func.attr)
    return fn


def _lookup_callable(fn: Callable[..., Any], name: str) -> Optional[Callable[..., Any]]:
    mod = inspect.getmodule(fn)
    if mod and hasattr(mod, name):
        obj = getattr(mod, name)
        if callable(obj):
            return obj
    globs = getattr(fn, "__globals__", {})
    obj = globs.get(name)
    return obj if callable(obj) else None


def _fn_source(fn: Callable[..., Any]) -> Optional[str]:
    try:
        lines, _ = inspect.getsourcelines(fn)
        return textwrap.dedent("".join(lines)).strip()
    except (OSError, TypeError):
        return None


def _compile_body(fn: Callable[..., Any], ctx: FrameCtx) -> List[Dict[str, Any]]:
    src = _fn_source(fn)
    if src is None:
        return []
    tree = ast.parse(src)
    if not tree.body or not isinstance(tree.body[0], ast.FunctionDef):
        return []
    ops: List[Dict[str, Any]] = []
    for stmt in tree.body[0].body:
        ops.extend(_stmt_ops(stmt, ctx))
    return ops


def _stmt_ops(stmt: ast.AST, ctx: FrameCtx) -> List[Dict[str, Any]]:
    if isinstance(stmt, ast.If):
        cond = _condition(stmt.test, ctx)
        if cond is None:
            return []
        if isinstance(stmt.test, ast.UnaryOp) and isinstance(stmt.test.op, ast.Not):
            inner = _condition(stmt.test.operand, ctx)
            if inner:
                cond = f"!({inner})"
        body: List[Dict[str, Any]] = []
        for s in stmt.body:
            body.extend(_stmt_ops(s, ctx))
        if not body and any(isinstance(s, ast.Return) for s in stmt.body):
            return [{"if": cond, "return": True}]
        return [{"if": cond, "ops": body}]
    if isinstance(stmt, ast.Return):
        return [{"return": True}]
    if isinstance(stmt, ast.For):
        return _for_ops(stmt, ctx)
    if isinstance(stmt, ast.Continue):
        return [{"continue": True}]
    if isinstance(stmt, ast.Break):
        return [{"break": True}]
    op = _assign_op(stmt, ctx)
    return [op] if op else []


def _for_ops(stmt: ast.For, ctx: FrameCtx) -> List[Dict[str, Any]]:
    if not isinstance(stmt.target, ast.Name) or stmt.target.id != "field":
        return []
    if not (isinstance(stmt.iter, ast.Call) and _name(stmt.iter) == "_obs_fields"):
        return []
    return [{"obs_loop": True, "ops": [_flatten_loop_body(s, ctx) for s in stmt.body]}]


def _flatten_loop_body(stmt: ast.AST, ctx: FrameCtx) -> Dict[str, Any]:
    ops = _stmt_ops(stmt, ctx)
    return ops[0] if len(ops) == 1 else {"block": ops}


def _assign_op(stmt: ast.AST, ctx: FrameCtx) -> Optional[Dict[str, Any]]:
    if isinstance(stmt, ast.AugAssign) and isinstance(stmt.target, ast.Name):
        if stmt.target.id == "ox":
            rhs = _num_expr(stmt.value, ctx)
            if rhs:
                return {"ox_sub": rhs}
    if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
        if isinstance(stmt.targets[0], ast.Name) and stmt.targets[0].id == "ox":
            return None
        sig = _assign_target_sig(stmt.targets[0], ctx)
        if not sig:
            return None
        if isinstance(stmt.value, ast.Constant):
            return {"set": sig, "v": stmt.value.value}
        if isinstance(stmt.value, ast.Call):
            call = stmt.value
            if isinstance(call.func, ast.Attribute) and call.func.attr == "uniform":
                lo = _num_expr(call.args[0], ctx)
                hi = _num_expr(call.args[1], ctx)
                if lo and hi:
                    return {"set": sig, "expr": f"({lo}+({hi}-({lo}))*Math.random())"}
        expr = _num_expr(stmt.value, ctx)
        if expr:
            return {"set": sig, "expr": expr}
    if isinstance(stmt, ast.AugAssign):
        sig = _assign_target_sig(stmt.target, ctx)
        if not sig:
            return None
        rhs = _num_expr(stmt.value, ctx)
        if not rhs:
            return None
        if isinstance(stmt.op, ast.Add):
            return {"add": sig, "expr": rhs}
        if isinstance(stmt.op, ast.Sub):
            return {"sub": sig, "expr": rhs}
    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
        call = stmt.value
        if _name(call.func) == "setattr" and len(call.args) >= 3:
            sig = _setattr_sig(call.args[0], call.args[1], ctx)
            if sig == "dynamic":
                expr = _num_expr(call.args[2], ctx) or "ox"
                if isinstance(call.args[2], ast.Name) and call.args[2].id == "ox":
                    return None
                return {"set_dynamic": True, "expr": expr}
            if not sig:
                return None
            if isinstance(call.args[2], ast.Constant):
                return {"set": sig, "v": call.args[2].value}
            expr = _num_expr(call.args[2], ctx)
            if expr:
                return {"set": sig, "expr": expr}
        if _name(call.func) == "_hit" and len(call.args) == 1:
            ox = _num_expr(call.args[0], ctx)
            if ox:
                return {"hit": ox}
    return None


def _assign_target_sig(node: ast.AST, ctx: FrameCtx) -> Optional[str]:
    sig = ctx.store_sig(node)
    if sig:
        return sig
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Call):
        cls = _call_store_class(node.value)
        if cls:
            return f"{cls}.{node.attr}"
    if isinstance(node, ast.Name) and node.id in ctx.aliases:
        return f"{ctx.store_class('x')}.{ctx.aliases[node.id]}" if False else None
    if isinstance(node, ast.Name) and node.id in ctx.aliases.values():
        return None
    if isinstance(node, ast.Name) and node.id in ctx.aliases:
        field = ctx.aliases[node.id]
        cls = ctx.store_class(next(iter(ctx.aliases))) or "RunnerStore"
        if "." not in field:
            return f"{cls}.{field}"
    return None


def _setattr_sig(obj: ast.AST, field: ast.AST, ctx: FrameCtx) -> Optional[str]:
    if isinstance(field, ast.Name) and field.id == "field":
        return "dynamic"
    if not isinstance(field, ast.Constant) or not isinstance(field.value, str):
        if isinstance(field, ast.Name) and field.id in ctx.aliases:
            fname = ctx.aliases[field.id]
        else:
            return None
    else:
        fname = field.value
    if isinstance(obj, ast.Name):
        cls = ctx.store_class(obj.id)
        if cls:
            return f"{cls}.{fname}"
    if isinstance(obj, ast.Call):
        cls = _call_store_class(obj)
        if cls:
            return f"{cls}.{fname}"
    return None


def _condition(node: ast.AST, ctx: FrameCtx) -> Optional[str]:
    if isinstance(node, ast.Call) and _name(node.func) == "_hit" and node.args:
        ox = _num_expr(node.args[0], ctx)
        return _hit_expr(ox, ctx) if ox else None
    sig = ctx.store_sig(node)
    if sig:
        return f"g('{sig}')"
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        inner = _condition(node.operand, ctx)
        return f"!({inner})" if inner else None
    if isinstance(node, ast.Compare) and len(node.ops) == 1:
        if isinstance(node.left, ast.Name) and node.left.id == "ox":
            right = _num_expr(node.comparators[0], ctx)
            op = {ast.Lt: "<", ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">="}.get(type(node.ops[0]))
            if right and op:
                return f"(ox{op}{right})"
        left = _num_expr(node.left, ctx)
        right = _num_expr(node.comparators[0], ctx)
        if left and right:
            op = {ast.Lt: "<", ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">="}.get(type(node.ops[0]))
            if op:
                return f"({left}{op}{right})"
    if isinstance(node, ast.Call) and _name(node.func) == "getattr" and len(node.args) >= 2:
        sig = _setattr_sig(node.args[0], node.args[1], ctx)
        if sig and sig != "dynamic":
            return f"g('{sig}')"
        if sig == "dynamic":
            return "ox"
    if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
        raw = [_condition(v, ctx) for v in node.values]
        parts: list[str] = []
        for p in raw:
            if p is not None:
                parts.append(p)
        if parts:
            return "||".join(parts)
    return None


def _num_expr(node: ast.AST, ctx: FrameCtx) -> Optional[str]:
    if isinstance(node, ast.Constant):
        return repr(node.value)
    if isinstance(node, ast.Name):
        if node.id == "dt":
            return "dt"
        if node.id == "ox":
            return "ox"
        if node.id in ctx.consts:
            return repr(ctx.consts[node.id])
        if node.id in ctx.aliases:
            field = ctx.aliases[node.id]
            cls = next((ctx.store_class(k) for k in ctx.aliases if ctx.store_class(k)), "RunnerStore")
            if cls and "." not in field:
                return f"g('{cls}.{field}')"
        cls = ctx.store_class(node.id)
        if cls:
            return f"g('{cls}')"
    sig = ctx.store_sig(node)
    if sig:
        return f"g('{sig}')"
    if isinstance(node, ast.Call):
        fname = _name(node.func)
        if fname in ("max", "min"):
            args = ", ".join(_num_expr(a, ctx) or "0" for a in node.args)
            return f"Math.{fname}({args})"
        if fname == "int" and node.args:
            inner = _num_expr(node.args[0], ctx)
            return f"Math.floor({inner})" if inner else None
        if fname == "getattr" and len(node.args) >= 2:
            sig = _setattr_sig(node.args[0], node.args[1], ctx)
            if sig == "dynamic":
                return "ox"
            if sig:
                return f"g('{sig}')"
        if fname == "_hit" and node.args:
            ox = _num_expr(node.args[0], ctx)
            return _hit_expr(ox, ctx) if ox else None
    if isinstance(node, ast.BinOp):
        left = _num_expr(node.left, ctx)
        right = _num_expr(node.right, ctx)
        if left and right:
            op = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/"}.get(type(node.op), "+")
            return f"({left}{op}{right})"
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        inner = _num_expr(node.operand, ctx)
        return f"(-{inner})" if inner else None
    return None


def _hit_expr(ox: str, ctx: FrameCtx) -> str:
    px = ctx.consts.get("PLAYER_X", 80)
    pw = ctx.consts.get("PLAYER_W", 32)
    ph = ctx.consts.get("PLAYER_H", 32)
    ow = ctx.consts.get("OBS_W", 28)
    gy = ctx.consts.get("GROUND_Y", 300)
    return (
        f"(({ox})+{ow}<{px}||({ox})>{px + pw})?false:"
        f"(g('RunnerStore.player_y')+{ph}>{gy + 4})"
    )


def _resolve_store_name(name: str, fn: Callable[..., Any]) -> Optional[str]:
    from echoui.state import Store

    globs = getattr(fn, "__globals__", {})
    obj = globs.get(name)
    if isinstance(obj, Store):
        return obj.__class__.__name__
    if name.endswith("Store"):
        return name
    return None


def _name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Call):
        return _name(node.func)
    return ""


def _emit_js(ops: List[Dict[str, Any]]) -> str:
    lines = ["function __echoui_frame(dt,S,s){", "function g(k){return S[k];}"]
    for op in ops:
        lines.extend(_emit_op(op, 1))
    lines.append("}")
    return "\n".join(lines)


def _emit_op(op: Dict[str, Any], indent: int) -> List[str]:
    sp = "  " * indent
    out: List[str] = []
    if "obs_loop" in op:
        out.append(f"{sp}for(var fi=0;fi<4;fi++){{")
        out.append(f"{sp}  var field='obs'+fi+'_x';")
        out.append(f"{sp}  var ox=g('RunnerStore.'+field);")
        for inner in op.get("ops", []):
            out.extend(_emit_obs_op(inner, indent + 1))
        out.append(f"{sp}}}")
        return out
    if "for_field" in op:
        return out
    if "if" in op:
        out.append(f"{sp}if({op['if']}){{")
        if op.get("return"):
            out.append(f"{sp}  return;")
        for inner in op.get("ops", []):
            out.extend(_emit_obs_op(inner, indent + 1))
        out.append(f"{sp}}}")
        return out
    if "return" in op:
        out.append(f"{sp}return;")
        return out
    if "continue" in op:
        return [f"{sp}continue;"]
    if "break" in op:
        return [f"{sp}break;"]
    if "hit" in op:
        out.append(f"{sp}if({_hit_expr(op['hit'], FrameCtx(fn=lambda: None, consts={'PLAYER_X':80,'PLAYER_W':32,'PLAYER_H':32,'OBS_W':28,'GROUND_Y':300}))}){{s('RunnerStore.game_over',true);return;}}")
        return out
    if "set" in op:
        sig = op["set"]
        if "v" in op:
            out.append(f"{sp}s('{sig}',{_js_val(op['v'])});")
        elif "expr" in op:
            out.append(f"{sp}s('{sig}',{op['expr']});")
        return out
    if "add" in op:
        out.append(f"{sp}s('{op['add']}',g('{op['add']}')+({op['expr']}));")
        return out
    if "sub" in op:
        out.append(f"{sp}s('{op['sub']}',g('{op['sub']}')-({op['expr']}));")
        return out
    if op.get("set_dynamic"):
        expr = op.get("expr") or "ox"
        out.append(f"{sp}s('RunnerStore.'+field,{expr});")
        return out
    if "ox_sub" in op:
        out.append(f"{sp}ox-=({op['ox_sub']});")
        out.append(f"{sp}s('RunnerStore.'+field,ox);")
        return out
    return out


def _emit_obs_op(op: Dict[str, Any], indent: int) -> List[str]:
    if "block" in op:
        lines: List[str] = []
        for inner in op["block"]:
            lines.extend(_emit_obs_op(inner, indent))
        return lines
    if op.get("continue"):
        return ["  " * indent + "continue;"]
    if "ox_sub" in op:
        return ["  " * indent + f"ox-=({op['ox_sub']});", "  " * indent + "s('RunnerStore.'+field,ox);"]
    if op.get("set_dynamic"):
        expr = op.get("expr") or "ox"
        return ["  " * indent + f"s('RunnerStore.'+field,{expr});"]
    if "hit" in op:
        hx = _hit_expr("ox", FrameCtx(fn=lambda: None, consts={"PLAYER_X": 80, "PLAYER_W": 32, "PLAYER_H": 32, "OBS_W": 28, "GROUND_Y": 300}))
        return ["  " * indent + f"if({hx}){{s('RunnerStore.game_over',true);return;}}"]
    if "if" in op:
        return _emit_op(op, indent)
    return _emit_op(op, indent)


def _js_val(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, str):
        return json_quote(v)
    return repr(v)


def json_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
