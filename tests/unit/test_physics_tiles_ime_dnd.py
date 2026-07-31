"""Physics (AABB + optional pymunk), TMX tiles, IME composition, file drop."""

from __future__ import annotations

import pytest

from echoui.events import DropFile, DropPayload, Event, dispatch_drop, make_drop_event
from echoui.input import CompositionState, apply_composition_event, keyboard
from echoui.physics import AABB, Body, World, create_world, pymunk_available
from echoui.tiles import TileMap, load_tmx, tilemap

SAMPLE_TMX = """<?xml version="1.0" encoding="UTF-8"?>
<map version="1.10" orientation="orthogonal" width="4" height="3" tilewidth="16" tileheight="16">
 <properties>
  <property name="author" value="echoui"/>
 </properties>
 <layer id="1" name="ground" width="4" height="3">
  <data encoding="csv">
1,1,1,1,
0,0,0,0,
0,0,0,0
  </data>
 </layer>
 <layer id="2" name="collision" width="4" height="3">
  <data encoding="csv">
1,1,1,1,
0,0,0,0,
0,0,0,0
  </data>
 </layer>
</map>
"""


def test_aabb_world_step_and_resolve():
    w = World(gravity=(0, 100))
    floor = Body(AABB(0, 100, 200, 10), static=True)
    box = Body(AABB(50, 0, 20, 20), vy=0)
    w.add(floor)
    w.add(box)
    for _ in range(30):
        w.step(0.05)
    assert box.aabb.y + box.aabb.h <= floor.aabb.y + 1.0
    assert create_world("aabb").gravity == (0, 980)


def test_create_world_unknown_backend():
    with pytest.raises(ValueError, match="unknown physics backend"):
        create_world("box2d")


@pytest.mark.skipif(not pymunk_available(), reason="pymunk optional extra not installed")
def test_pymunk_world_circle_falls():
    world = create_world("pymunk", gravity=(0, 900))
    world.add_box(0, 200, 400, 20, static=True)  # type: ignore[union-attr]
    world.add_circle(0, 0, 10, mass=1.0, elasticity=0.0)  # type: ignore[union-attr]
    y0 = world.positions()[0][1]  # type: ignore[union-attr]
    for _ in range(40):
        world.step(1 / 60)  # type: ignore[union-attr]
    y1 = world.positions()[0][1]  # type: ignore[union-attr]
    assert y1 > y0


def test_tilemap_basic_and_layer_api():
    tm = tilemap(3, 2, tile_size=32, fill=0)
    tm.set(1, 0, 5)
    assert tm.get(1, 0) == 5
    assert tm.world_to_tile(40, 10) == (1, 0)


def test_load_tmx_csv_layers_and_solid():
    tm = load_tmx(SAMPLE_TMX)
    assert isinstance(tm, TileMap)
    assert tm.cols == 4 and tm.rows == 3
    assert tm.tile_width == 16
    assert tm.properties.get("author") == "echoui"
    ground = tm.layer("ground")
    assert ground.get(0, 0) == 1
    assert ground.get(0, 1) == 0
    col = tm.layer("collision")
    assert col.solid is True
    assert tm.solid_at(0, 0) is True
    assert tm.solid_at(0, 1) is False


def test_load_tmx_base64_uncompressed():
    import base64
    import struct

    # 2x1 map: GIDs 1, 2 as little-endian u32
    raw = struct.pack("<2I", 1, 2)
    b64 = base64.b64encode(raw).decode("ascii")
    tmx = f"""<?xml version="1.0" encoding="UTF-8"?>
<map version="1.10" orientation="orthogonal" width="2" height="1" tilewidth="8" tileheight="8">
 <layer id="1" name="ground" width="2" height="1">
  <data encoding="base64">{b64}</data>
 </layer>
</map>
"""
    tm = load_tmx(tmx)
    assert tm.get(0, 0) == 1
    assert tm.get(1, 0) == 2


def test_load_tmx_base64_gzip():
    import base64
    import gzip
    import struct

    raw = struct.pack("<4I", 3, 0, 0, 4)
    b64 = base64.b64encode(gzip.compress(raw)).decode("ascii")
    tmx = f"""<map width="2" height="2" tilewidth="8" tileheight="8">
 <layer name="ground" width="2" height="2">
  <data encoding="base64" compression="gzip">{b64}</data>
 </layer>
</map>"""
    tm = load_tmx(tmx)
    assert tm.get(0, 0) == 3
    assert tm.get(1, 1) == 4


def test_load_tmx_rejects_unknown_encoding():
    bad = """<map width="1" height="1" tilewidth="8" tileheight="8">
 <layer name="a" width="1" height="1"><data encoding="xml">0</data></layer>
</map>"""
    with pytest.raises(ValueError, match="CSV or base64"):
        load_tmx(bad)


def test_load_tmx_rejects_infinite():
    bad = """<map width="2" height="2" tilewidth="8" tileheight="8" infinite="1">
 <layer name="a" width="2" height="2"><data encoding="csv">0,0,0,0</data></layer>
</map>"""
    with pytest.raises(ValueError, match="infinite"):
        load_tmx(bad)


SAMPLE_TMX_OBJECTS = """<?xml version="1.0" encoding="UTF-8"?>
<map version="1.10" orientation="orthogonal" width="4" height="3" tilewidth="16" tileheight="16">
 <layer id="1" name="ground" width="4" height="3">
  <data encoding="csv">
1,1,1,1,
0,0,0,0,
0,0,0,0
  </data>
 </layer>
 <objectgroup id="2" name="spawns" opacity="0.9">
  <object id="10" name="player" type="spawn" x="24" y="40" width="16" height="16">
   <properties>
    <property name="facing" value="right"/>
   </properties>
  </object>
  <object id="11" name="checkpoint" x="80" y="48">
   <point/>
  </object>
  <object id="12" name="gate" gid="5" x="100" y="20" width="16" height="16"/>
  <object id="13" name="oval" x="10" y="10" width="20" height="10">
   <ellipse/>
  </object>
  <object id="14" name="poly" x="5" y="6">
   <polygon points="0,0 10,0 10,8 0,8"/>
  </object>
  <object id="15" name="path" x="50" y="60">
   <polyline points="0,0 4,2 8,-1"/>
  </object>
 </objectgroup>
 <objectgroup id="3" name="triggers">
  <object id="20" name="zone" class="trigger" x="0" y="0" width="32" height="32"/>
 </objectgroup>
</map>
"""


def test_load_tmx_object_layers_points_rects_and_props():
    from echoui.tiles import MapObject, ObjectGroup

    tm = load_tmx(SAMPLE_TMX_OBJECTS)
    assert len(tm.object_groups) == 2
    spawns = tm.object_group("spawns")
    assert isinstance(spawns, ObjectGroup)
    assert spawns.opacity == pytest.approx(0.9)
    player = spawns.get("player")
    assert isinstance(player, MapObject)
    assert player.type == "spawn"
    assert player.x == 24 and player.y == 40
    assert player.is_rect is True
    assert player.properties.get("facing") == "right"
    assert player.object_id == 10

    cp = tm.find_object("checkpoint")
    assert cp.is_point is True
    assert cp.width == 0 and cp.height == 0

    gate = tm.find_object("gate", group="spawns")
    assert gate.gid == 5

    oval = spawns.get("oval")
    assert oval.type == "ellipse"

    poly = spawns.get("poly")
    assert poly.is_polygon is True
    assert poly.points == [(0.0, 0.0), (10.0, 0.0), (10.0, 8.0), (0.0, 8.0)]
    assert poly.absolute_points() == [(5.0, 6.0), (15.0, 6.0), (15.0, 14.0), (5.0, 14.0)]
    assert poly.is_rect is False
    assert poly.is_point is False

    path = spawns.get("path")
    assert path.is_polyline is True
    assert path.points == [(0.0, 0.0), (4.0, 2.0), (8.0, -1.0)]
    assert path.absolute_points()[1] == (54.0, 62.0)

    triggers = tm.object_group("triggers").by_type("trigger")
    assert len(triggers) == 1
    assert triggers[0].name == "zone"

    all_objs = tm.objects()
    assert len(all_objs) == 7
    assert tm.find_object("player").name == "player"
    with pytest.raises(KeyError):
        tm.object_group("missing")
    with pytest.raises(KeyError):
        tm.find_object("nope")


def test_ime_composition_on_keyboard():
    keyboard.composition.clear()
    keyboard.take_committed()
    assert keyboard.composing() is False
    apply_composition_event("compositionstart", "")
    assert keyboard.composing() is True
    apply_composition_event("compositionupdate", "ni")
    assert keyboard.composition_text() == "ni"
    committed = apply_composition_event("compositionend", "你")
    assert committed == "你"
    assert keyboard.composing() is False
    assert keyboard.take_committed() == ["你"]


def test_composition_state_unit():
    st = CompositionState()
    st.begin("a")
    st.update("ab")
    assert st.active and st.data == "ab"
    assert st.end_session("完") == "完"
    assert not st.active


def test_make_drop_event_and_dispatch():
    ev = make_drop_event(
        x=10,
        y=20,
        files=[{"name": "a.png", "size": 12, "type": "image/png"}, "b.txt"],
        data="hello",
    )
    assert ev.type == "drop"
    assert ev.x == 10 and ev.y == 20
    assert len(ev.files) == 2
    assert isinstance(ev.files[0], DropFile)
    assert ev.files[0].name == "a.png"
    assert ev.files[1].name == "b.txt"

    seen: list[Event] = []

    def handler(e: Event) -> None:
        seen.append(e)

    registry = {"h1": handler}
    dom = [{"node": "n1", "type": "drop", "handler": "h1"}]
    ok = dispatch_drop(
        registry,
        dom,
        "n1",
        DropPayload(x=1, y=2, files=[DropFile(name="z.bin", size=3)]),
    )
    assert ok is True
    assert len(seen) == 1
    assert seen[0].files[0].name == "z.bin"
    assert dispatch_drop(registry, dom, "missing") is False


def test_drop_target_collected_into_client_cfg():
    from echoui.compiler.client_cfg import build_client_cfg
    from echoui.compiler.lower import lower_web
    from echoui.compiler.ui_collect import analyze_ui
    from echoui.layout import drop_target, text
    from echoui.sprite import reset_id_gen

    reset_id_gen()
    root = drop_target(
        text("drop here"),
        signal="App.drop_meta",
        file_signal="App.file_url",
        effect="copy",
        preview_id="prev1",
    )
    bindings, signals, files, overlays, drops = analyze_ui(root)
    assert len(drops) == 1
    d = drops[0]
    assert d["node"] == root.id
    assert d["signal"] == "App.drop_meta"
    assert d["fileSignal"] == "App.file_url"
    assert d["effect"] == "copy"
    assert d["previewNode"] == "prev1"

    lowered = lower_web(
        {
            "root": root,
            "ir": {"app": {}},
            "drop_targets": drops,
            "file_inputs": files,
            "overlays": overlays,
            "signals": signals,
            "reactive_bindings": bindings,
        }
    )
    assert lowered["drop_targets"] == drops
    cfg = build_client_cfg(lowered)
    assert cfg["drop_targets"][0]["signal"] == "App.drop_meta"


def test_astar_on_tilemap_avoids_solid():
    from echoui.pathfind import astar_on_tilemap

    tm = load_tmx(SAMPLE_TMX)
    # row0 solid; path must go through open cells row1/2
    path = astar_on_tilemap(tm, (0, 1), (3, 1))
    assert path is not None
    assert path[0] == (0, 1) and path[-1] == (3, 1)
    for x, y in path:
        assert tm.solid_at(x, y) is False
