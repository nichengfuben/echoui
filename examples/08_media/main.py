"""Media demo — HTML5 video + audio roles."""

from __future__ import annotations

from echoui import App, Screen, Store, audio_player, col, heading, text, video

class MediaStore(Store):
    note: str = "HTML5 media roles"


store = MediaStore()


class Media(Screen):
    layout = "flow"

    def build(self):
        return col(
            heading("EchoUI Media"),
            text(lambda: store.note),
            video(
                src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
                width=480,
                height=270,
            ),
            audio_player(src="https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3"),
        )


app = App(screens=[Media], initial="Media")
