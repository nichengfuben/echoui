from echoui import App, Screen, Store, button, col, text
from echoui.raw import RawBridge, js
from echoui.reactive import Signal

bridge = RawBridge()
value = Signal(0)

class EscapeStore(Store):
    label: str = "initial"

store = EscapeStore()

_raw_code = """
(function(){
  var el = document.getElementById('escape-out');
  if(el) el.textContent = 'raw.js loaded';
})();
"""

class Escape(Screen):
    def build(self):
        bridge.register("escape", lambda: store.__setattr__("label", "mounted"))
        return col(
            text(lambda: f"Signal: {store.label}"),
            js(_raw_code),
            button("Bump", on_click=lambda: setattr(store, "label", store.label + "!")),
        )

app = App(screens=[Escape], initial="Escape")
