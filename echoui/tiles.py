"""Tile map utilities and TMX (Tiled) subset loader."""

from __future__ import annotations

import base64
import gzip
import struct
import xml.etree.ElementTree as ET
import zlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union


@dataclass
class TileLayer:
    """One named layer of tile GIDs (row-major, 0 = empty)."""

    name: str
    cols: int
    rows: int
    data: List[int]
    solid: bool = False
    visible: bool = True
    opacity: float = 1.0

    def get(self, col: int, row: int) -> int:
        if col < 0 or row < 0 or col >= self.cols or row >= self.rows:
            return -1
        return self.data[row * self.cols + col]

    def set(self, col: int, row: int, value: int) -> None:
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.data[row * self.cols + col] = value

    def is_solid_at(self, col: int, row: int) -> bool:
        if not self.solid:
            return False
        gid = self.get(col, row)
        return gid > 0


@dataclass
class MapObject:
    """One Tiled object (point / rectangle / tile-ref / polygon-polyline subset)."""

    name: str = ""
    type: str = ""
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    gid: Optional[int] = None
    object_id: Optional[int] = None
    visible: bool = True
    properties: Dict[str, str] = field(default_factory=dict)
    # Polygon/polyline vertices relative to (x, y); empty for point/rect/tile.
    points: List[tuple[float, float]] = field(default_factory=list)

    @property
    def is_point(self) -> bool:
        return (
            self.width <= 0
            and self.height <= 0
            and self.gid is None
            and not self.points
        )

    @property
    def is_rect(self) -> bool:
        return self.width > 0 and self.height > 0 and not self.points

    @property
    def is_polygon(self) -> bool:
        return self.type == "polygon" and bool(self.points)

    @property
    def is_polyline(self) -> bool:
        return self.type == "polyline" and bool(self.points)

    def absolute_points(self) -> List[tuple[float, float]]:
        """Return vertices in map coordinates (object origin + relative points)."""
        return [(self.x + px, self.y + py) for px, py in self.points]


@dataclass
class ObjectGroup:
    """Named object layer (``<objectgroup>``)."""

    name: str
    objects: List[MapObject] = field(default_factory=list)
    visible: bool = True
    opacity: float = 1.0

    def get(self, name: str) -> MapObject:
        for obj in self.objects:
            if obj.name == name:
                return obj
        raise KeyError(f"map object not found: {name!r}")

    def by_type(self, type_name: str) -> List[MapObject]:
        return [o for o in self.objects if o.type == type_name]


@dataclass
class TileMap:
    cols: int
    rows: int
    tile_size: int
    data: List[int]
    layers: List[TileLayer] = field(default_factory=list)
    object_groups: List[ObjectGroup] = field(default_factory=list)
    tile_width: Optional[int] = None
    tile_height: Optional[int] = None
    properties: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.tile_width is None:
            self.tile_width = self.tile_size
        if self.tile_height is None:
            self.tile_height = self.tile_size
        if not self.layers and self.data:
            self.layers = [
                TileLayer(
                    name="default",
                    cols=self.cols,
                    rows=self.rows,
                    data=list(self.data),
                    solid=False,
                )
            ]

    def layer(self, name: str) -> TileLayer:
        for lay in self.layers:
            if lay.name == name:
                return lay
        raise KeyError(f"tile layer not found: {name!r}")

    def object_group(self, name: str) -> ObjectGroup:
        for grp in self.object_groups:
            if grp.name == name:
                return grp
        raise KeyError(f"object group not found: {name!r}")

    def objects(self, group: Optional[str] = None) -> List[MapObject]:
        if group is None:
            out: List[MapObject] = []
            for grp in self.object_groups:
                out.extend(grp.objects)
            return out
        return list(self.object_group(group).objects)

    def find_object(self, name: str, group: Optional[str] = None) -> MapObject:
        for obj in self.objects(group):
            if obj.name == name:
                return obj
        raise KeyError(f"map object not found: {name!r}")

    def get(self, col: int, row: int) -> int:
        if self.layers:
            return self.layers[0].get(col, row)
        if col < 0 or row < 0 or col >= self.cols or row >= self.rows:
            return -1
        return self.data[row * self.cols + col]

    def set(self, col: int, row: int, value: int) -> None:
        if self.layers:
            self.layers[0].set(col, row, value)
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.data[row * self.cols + col] = value

    def world_to_tile(self, x: float, y: float) -> tuple[int, int]:
        tw = self.tile_width or self.tile_size
        th = self.tile_height or self.tile_size
        return int(x // tw), int(y // th)

    def tile_to_world(self, col: int, row: int) -> tuple[float, float]:
        tw = self.tile_width or self.tile_size
        th = self.tile_height or self.tile_size
        return col * tw, row * th

    def solid_at(self, col: int, row: int) -> bool:
        for lay in self.layers:
            if lay.is_solid_at(col, row):
                return True
        return False


def tilemap(cols: int, rows: int, tile_size: int = 32, fill: int = 0) -> TileMap:
    return TileMap(cols=cols, rows=rows, tile_size=tile_size, data=[fill] * (cols * rows))


def _parse_csv_data(text: str, cols: int, rows: int) -> List[int]:
    raw = [p.strip() for p in text.replace("\n", ",").split(",") if p.strip() != ""]
    values = [int(p) for p in raw]
    expected = cols * rows
    if len(values) < expected:
        values.extend([0] * (expected - len(values)))
    return values[:expected]


def _parse_base64_data(text: str, cols: int, rows: int, compression: str = "") -> List[int]:
    """Decode Tiled base64 layer (optional gzip/zlib); GIDs are little-endian u32."""
    raw = base64.b64decode("".join((text or "").split()))
    comp = (compression or "").lower()
    if comp in ("gzip", "gz"):
        raw = gzip.decompress(raw)
    elif comp in ("zlib", "zstd"):  # zstd not stdlib — reject below
        if comp == "zstd":
            raise ValueError("TMX compression 'zstd' is not supported")
        raw = zlib.decompress(raw)
    elif comp:
        raise ValueError(f"TMX compression {comp!r} is not supported")
    expected = cols * rows
    need = expected * 4
    if len(raw) < need:
        raw = raw + b"\x00" * (need - len(raw))
    values = list(struct.unpack_from(f"<{expected}I", raw, 0))
    return values


def _parse_layer_data(data_el: ET.Element, cols: int, rows: int, layer_name: str) -> List[int]:
    enc = (data_el.get("encoding") or "csv").lower()
    if enc == "csv":
        return _parse_csv_data(data_el.text or "", cols, rows)
    if enc == "base64":
        return _parse_base64_data(
            data_el.text or "",
            cols,
            rows,
            compression=data_el.get("compression") or "",
        )
    raise ValueError(
        f"TMX layer {layer_name!r}: only CSV or base64 encoding is supported (got {enc!r})"
    )


def _layer_solid_flag(layer_el: ET.Element) -> bool:
    name = (layer_el.get("name") or "").lower()
    if "collision" in name or name in ("solid", "solids", "walls"):
        return True
    for prop in layer_el.findall("./properties/property"):
        pname = (prop.get("name") or "").lower()
        pval = (prop.get("value") or "").lower()
        if pname in ("solid", "collision", "collidable") and pval in (
            "1",
            "true",
            "yes",
        ):
            return True
    return False


def _parse_properties(el: ET.Element) -> Dict[str, str]:
    props: Dict[str, str] = {}
    for prop in el.findall("./properties/property"):
        if prop.get("name"):
            props[prop.get("name") or ""] = prop.get("value") or (prop.text or "")
    return props


def _parse_points_attr(text: str) -> List[tuple[float, float]]:
    """Parse Tiled ``points="x,y x,y ..."`` into relative vertex list."""
    out: List[tuple[float, float]] = []
    for part in (text or "").replace(";", " ").split():
        if "," not in part:
            continue
        xs, ys = part.split(",", 1)
        try:
            out.append((float(xs), float(ys)))
        except ValueError:
            continue
    return out


def _parse_map_object(obj_el: ET.Element) -> MapObject:
    """Parse ``<object>`` point / rect / tile-gid / polygon / polyline vertices."""
    oid_raw = obj_el.get("id")
    oid = int(oid_raw) if oid_raw not in (None, "") else None
    gid_raw = obj_el.get("gid")
    gid = int(gid_raw) if gid_raw not in (None, "") else None
    w = float(obj_el.get("width", "0") or 0)
    h = float(obj_el.get("height", "0") or 0)
    # Tiled marks points with empty <point/> child or zero size without gid.
    has_point = obj_el.find("point") is not None
    if has_point:
        w, h = 0.0, 0.0
    typ = obj_el.get("type") or obj_el.get("class") or ""
    points: List[tuple[float, float]] = []
    if obj_el.find("ellipse") is not None and not typ:
        typ = "ellipse"
    poly_el = obj_el.find("polygon")
    if poly_el is not None:
        if not typ:
            typ = "polygon"
        points = _parse_points_attr(poly_el.get("points") or "")
    line_el = obj_el.find("polyline")
    if line_el is not None:
        if not typ:
            typ = "polyline"
        points = _parse_points_attr(line_el.get("points") or "")
    visible = obj_el.get("visible", "1") not in ("0", "false")
    return MapObject(
        name=obj_el.get("name") or "",
        type=typ,
        x=float(obj_el.get("x", "0") or 0),
        y=float(obj_el.get("y", "0") or 0),
        width=w,
        height=h,
        gid=gid,
        object_id=oid,
        visible=visible,
        properties=_parse_properties(obj_el),
        points=points,
    )


def _parse_object_group(group_el: ET.Element) -> ObjectGroup:
    name = group_el.get("name") or "objects"
    visible = group_el.get("visible", "1") not in ("0", "false")
    opacity = float(group_el.get("opacity", "1"))
    objects = [_parse_map_object(o) for o in group_el.findall("object")]
    return ObjectGroup(name=name, objects=objects, visible=visible, opacity=opacity)


def load_tmx(source: Union[str, bytes], *, encoding: str = "utf-8") -> TileMap:
    """Load a Tiled TMX subset (orthogonal maps).

    Supports: map size, tilewidth/height, multiple ``<layer>`` with CSV or
    base64 ``<data>`` (optional gzip/zlib compression), layer ``solid`` via
    name containing ``collision`` or property ``solid=true``, and
    ``<objectgroup>`` point/rectangle/tile/polygon/polyline objects
    (properties and vertex lists included). Infinite maps and zstd are not
    supported.
    """
    if isinstance(source, bytes):
        text = source.decode(encoding)
    else:
        text = source
        # path vs inline XML
        stripped = text.lstrip()
        if not stripped.startswith("<") and "\n" not in text[:80] and len(text) < 4096:
            try:
                with open(text, encoding=encoding) as f:
                    text = f.read()
            except OSError:
                pass
    root = ET.fromstring(text)
    if root.tag != "map":
        raise ValueError("TMX root must be <map>")
    if (root.get("infinite") or "0") in ("1", "true"):
        raise ValueError("TMX infinite maps are not supported")
    cols = int(root.get("width", "0"))
    rows = int(root.get("height", "0"))
    tw = int(root.get("tilewidth", "32"))
    th = int(root.get("tileheight", tw))
    if cols <= 0 or rows <= 0:
        raise ValueError("TMX map width/height must be positive")
    props = _parse_properties(root)
    layers: List[TileLayer] = []
    for layer_el in root.findall("layer"):
        name = layer_el.get("name") or f"layer{len(layers)}"
        lc = int(layer_el.get("width", cols))
        lr = int(layer_el.get("height", rows))
        data_el = layer_el.find("data")
        if data_el is None:
            data = [0] * (lc * lr)
        else:
            data = _parse_layer_data(data_el, lc, lr, name)
        visible = layer_el.get("visible", "1") not in ("0", "false")
        opacity = float(layer_el.get("opacity", "1"))
        layers.append(
            TileLayer(
                name=name,
                cols=lc,
                rows=lr,
                data=data,
                solid=_layer_solid_flag(layer_el),
                visible=visible,
                opacity=opacity,
            )
        )
    object_groups = [_parse_object_group(g) for g in root.findall("objectgroup")]
    primary = layers[0].data if layers else [0] * (cols * rows)
    return TileMap(
        cols=cols,
        rows=rows,
        tile_size=tw,
        data=list(primary),
        layers=layers,
        object_groups=object_groups,
        tile_width=tw,
        tile_height=th,
        properties=props,
    )
