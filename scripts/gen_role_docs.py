#!/usr/bin/env python3
"""Generate docs-src role catalog from ROLE_MAP + emit_roles coverage."""

from __future__ import annotations

from pathlib import Path

from echoui.compiler.emit_roles import render_role_html
from echoui.roles import ROLE_MAP

SKIP = {"screen", "stage", "native", "raw"}
OUT = Path(__file__).resolve().parents[1] / "docs-src" / "echoui" / "api" / "roles" / "role-catalog.md"


def _emit_ok(role: str) -> bool:
    node = {
        "id": f"n_{role}",
        "role": role,
        "tag": ROLE_MAP.get(role, "div"),
        "props": {"text": "x", "label": "L", "name": "f", "options": [{"value": "a", "label": "A"}]},
        "children": [],
    }
    html = render_role_html(
        node, attrs=' id="n"', cls=f"e-{role}", style_attr="", inner="", kids=""
    )
    if html:
        return True
    from echoui.compiler.emit_web import _render_node

    return bool(_render_node(node))


def main() -> None:
    lines = [
        "# 内建 Role 全量图鉴",
        "",
        "> 自动生成：`python scripts/gen_role_docs.py`",
        "",
        "| role | HTML tag | Web emit | 测试 |",
        "|------|----------|:--------:|:----:|",
    ]
    ok = 0
    for role in sorted(ROLE_MAP):
        tag = ROLE_MAP[role]
        emitted = _emit_ok(role)
        if emitted:
            ok += 1
        mark = "✓" if emitted else "—"
        skip = role in SKIP
        test = "—" if skip else "test_all_roles_emit"
        lines.append(f"| `{role}` | `{tag}` | {mark} | {test} |")
    lines.extend(
        [
            "",
            f"**合计**：{len(ROLE_MAP)} roles，{ok} 可 emit HTML。",
            "",
            "专项文档：[media-upload.md](media-upload.md) · [text-button.md](text-button.md)",
        ]
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(ROLE_MAP)} roles, {ok} emit)")


if __name__ == "__main__":
    main()
