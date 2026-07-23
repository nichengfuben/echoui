"""Create package directory skeleton with minimal __init__.py stubs."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODULES = [
    "echoui/forms",
    "echoui/storage",
    "echoui/api",
    "echoui/graphql",
    "echoui/rpc",
    "echoui/rtc",
    "echoui/query",
    "echoui/router",
    "echoui/three",
    "echoui/audio",
    "echoui/media",
    "echoui/platform",
    "echoui/desktop",
    "echoui/mobile",
    "echoui/data",
    "echoui/i18n",
    "echoui/a11y",
    "echoui/print",
    "echoui/collab",
    "echoui/bridge",
    "echoui/compiler",
    "echoui/runtime",
    "echoui/targets",
    "echoui/contrib",
    "echoui/testing",
    "tests/unit",
    "tests/integration",
    "examples/02_counter",
    "examples/04_multi_screen_game",
    "examples/05_escape_layer",
    "docs-src/echoui/api",
    "docs-src/tests/unit",
]

STUBS: dict[str, str] = {
    "echoui/forms": "Form fields and validators.",
    "echoui/storage": "Client-side storage APIs.",
    "echoui/api": "HTTP and WebSocket client.",
    "echoui/query": "Stale-while-revalidate query layer.",
    "echoui/router": "Application router.",
    "echoui/bridge": "Native and web escape bridges.",
    "echoui/targets": "Per-target build orchestration.",
    "echoui/collab": "CRDT collaboration.",
    "echoui/data": "Tables and virtualized lists.",
    "echoui/i18n": "Internationalization.",
    "echoui/a11y": "Accessibility helpers.",
    "echoui/testing": "mount/fire test harness.",
}


def main() -> None:
    for rel in MODULES:
        d = ROOT / rel
        d.mkdir(parents=True, exist_ok=True)
        if rel.startswith("echoui/") and rel.count("/") == 1:
            init = d / "__init__.py"
            if not init.exists():
                doc = STUBS.get(rel, f"EchoUI package: {rel.split('/', 1)[1]}.")
                init.write_text(f'"""{doc}"""\n', encoding="utf-8")


if __name__ == "__main__":
    main()
