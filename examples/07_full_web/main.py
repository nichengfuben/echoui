"""Full web dashboard — Chart.js, MapLibre, OPFS storage, forms."""

from __future__ import annotations

from echoui import App, Screen, Store, button, chart, col, heading, input_field, map, text
from echoui.forms import Form, email, field, required
from echoui.raw import js

class DashStore(Store):
    name: str = ""
    email: str = ""
    status: str = "Ready"


store = DashStore()
form = Form().add(field("name", required())).add(field("email", email()))  # Python-side validation API demo

_load = js(
    """
(function(){
  var st=window.__echoui&&window.__echoui.storage;
  if(!st||!window.__echoui)return;
  var n=st.get('dash_name'),e=st.get('dash_email');
  var p={};
  if(n)p['DashStore.name']=n;
  if(e)p['DashStore.email']=e;
  if(Object.keys(p).length)window.__echoui.apply(p);
})();
"""
)

_save = js(
    """
(function(){
  document.addEventListener('click',function(ev){
    var t=ev.target;
    if(!t||!t.classList||!t.classList.contains('e-save-dash'))return;
    var st=window.__echoui&&window.__echoui.storage,g=window.__echoui.g;
    if(!st||!g)return;
    st.set('dash_name',g('DashStore.name')||'');
    st.set('dash_email',g('DashStore.email')||'');
    window.__echoui.apply({'DashStore.status':'Saved '+new Date().toLocaleTimeString()});
  });
})();
"""
)


class Dashboard(Screen):
    layout = "flow"

    def build(self):
        return col(
            heading("EchoUI Full Web Dashboard"),
            _load,
            _save,
            input_field("name", label="Name"),
            input_field("email", label="Email"),
            text(lambda: f"Status: {store.status}"),
            chart(data=[12, 19, 8, 15, 22, 17], width=420, height=220, production=True),
            map(lat=31.23, lng=121.47, zoom=10, width=500, height=300, production=True),
            button("Mark valid", on_click=lambda: setattr(store, "status", "Form valid")),
            button("Save to storage", css_class="e-save-dash"),
            text(lambda: f"Name: {store.name or '—'} · Email: {store.email or '—'}"),
        )


app = App(screens=[Dashboard], initial="Dashboard")
