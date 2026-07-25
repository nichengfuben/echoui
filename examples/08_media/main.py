"""Media demo — upload, costumes, video + audio."""

from __future__ import annotations

from echoui import (
    App,
    Screen,
    Store,
    audio_player,
    button,
    col,
    file_input,
    heading,
    image,
    text,
    video,
)
from echoui.costume import CostumeFieldsMixin, bind_costumes, costume


class MediaStore(Store, CostumeFieldsMixin):
    note: str = "Upload PNG → Save costume → Next / switch by name"
    sprite_url: str = ""


store = MediaStore()
controls = bind_costumes(
    MediaStore,
    [
        costume("idle", ""),
        costume("run", ""),
    ],
    url="sprite_url",
)


class Media(Screen):
    layout = "flow"

    def build(self):
        return col(
            heading("EchoUI Media"),
            text(lambda: store.note),
            text(lambda: f"Current: {store.current_costume or '—'}"),
            image(lambda: store.sprite_url, width=128, height=128),
            file_input("sprite", accept="image/*", signal="MediaStore.sprite_url", label="Sprite PNG"),
            button("Save costume", on_click=controls.save_costume),
            button("Next costume", on_click=controls.next_costume),
            button("Idle", on_click=controls.switch["idle"]),
            button("Run", on_click=controls.switch["run"]),
            video(
                src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
                width=480,
                height=270,
            ),
            audio_player(src="https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3"),
        )


app = App(screens=[Media], initial="Media")
