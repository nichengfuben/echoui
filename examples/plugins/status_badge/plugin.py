"""Third-party plugin example."""

from __future__ import annotations

from echoui import Screen, badge, col, text
from echoui.plugin import Plugin, role


@role("status_chip")
def render_status_chip(sprite, target: str) -> dict:
    return {"role": "status_chip", "target": target}


class StatusBadgePlugin(Plugin):
    name = "status_badge"


class Status(Screen):
    def build(self):
        return col(text("Plugin demo"), badge("NEW"))


def register() -> None:
    from echoui.plugin import register as register_plugin

    register_plugin(StatusBadgePlugin.name)
