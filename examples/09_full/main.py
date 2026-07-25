"""Full role showcase — forms, virtual list, file upload, overlays."""

from __future__ import annotations

from echoui import (
    App,
    Screen,
    Store,
    badge,
    button,
    card,
    checkbox,
    col,
    file_input,
    heading,
    image,
    input_field,
    progress,
    row,
    select,
    spinner,
    table,
    text,
    virtual_list,
)
from echoui.forms import Form, field, file_size, file_type, required
from echoui.i18n import load_catalog, set_locale, t
from echoui.overlay import modal

set_locale("en")
load_catalog("en", {"upload": "Upload avatar", "status": "Status: {s}"})


class FullStore(Store):
    avatar: str = ""
    progress: int = 40
    status: str = "idle"
    show_about: bool = False


store = FullStore()
form = Form().add(field("avatar", required(), file_type("image/"), file_size(5_000_000)))


class Full(Screen):
    layout = "flow"

    def build(self):
        return col(
            heading("EchoUI Full Showcase"),
            text(lambda: t("status", s=store.status)),
            card(
                row(
                    input_field("name", label="Name"),
                    select(name="role", options=[{"value": "dev", "label": "Developer"}]),
                    checkbox(label="Subscribe"),
                ),
                file_input("avatar", accept="image/*", label=t("upload"), signal="FullStore.avatar"),
                image(lambda: store.avatar or "", alt="preview", width=64, height=64),
                progress(value=store.progress, max=100),
                spinner(),
                badge("Beta"),
            ),
            table(
                columns=[{"key": "name", "label": "Name"}, {"key": "role", "label": "Role"}],
                rows=[{"name": "Alice", "role": "Dev"}, {"name": "Bob", "role": "Ops"}],
            ),
            virtual_list(total=1000, item_height=32, height=200),
            button("Validate", on_click=lambda: setattr(store, "status", "valid")),
            modal(col(heading("About"), text("EchoUI 1.2.1 full role showcase")), open_signal="FullStore.show_about"),
            button("About", on_click=lambda: setattr(store, "show_about", True)),
        )


app = App(screens=[Full], initial="Full")
