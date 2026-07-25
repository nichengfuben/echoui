"""Sprite costumes: costume(), switch_costume, next_costume."""

from __future__ import annotations

import textwrap
from dataclasses import dataclass
from typing import Callable, Dict, List, Sequence, Tuple, Type

from echoui.state import Store

MAX_COSTUMES = 8


@dataclass(frozen=True)
class Costume:
    name: str
    src: str


def costume(name: str, src: str) -> Costume:
    """Declare one named costume."""
    return Costume(name=name, src=src)


class CostumeFieldsMixin:
    """Store fields for :func:`bind_costumes` (up to 8 slots)."""

    costume_count: int = 0
    costume_index: int = 0
    current_costume: str = ""
    costume_name0: str = ""
    costume_name1: str = ""
    costume_name2: str = ""
    costume_name3: str = ""
    costume_name4: str = ""
    costume_name5: str = ""
    costume_name6: str = ""
    costume_name7: str = ""
    costume0: str = ""
    costume1: str = ""
    costume2: str = ""
    costume3: str = ""
    costume4: str = ""
    costume5: str = ""
    costume6: str = ""
    costume7: str = ""


_SLOT_FIELDS = tuple(f"costume{i}" for i in range(MAX_COSTUMES))
_NAME_FIELDS = tuple(f"costume_name{i}" for i in range(MAX_COSTUMES))


@dataclass
class CostumeControls:
    """Compile-local costume switchers bound to a Store."""

    store_cls: Type[Store]
    url_field: str
    names: Tuple[str, ...]
    next_costume: Callable[[], None]
    save_costume: Callable[[], None]
    switch: Dict[str, Callable[[], None]]

    def src(self, store_instance: Store) -> Callable[[], str]:
        field = self.url_field

        def _src() -> str:
            return getattr(store_instance, field)

        return _src


def _validate_field(name: str) -> None:
    if not name.isidentifier():
        raise ValueError(f"field must be a valid identifier, got {name!r}")


def _attach_source(fn: Callable[..., None], src: str) -> Callable[..., None]:
    fn.__echoui_source__ = src  # type: ignore[attr-defined]
    return fn


def _exec_handlers(store_name: str, store_cls: Type[Store], blocks: str) -> dict:
    ns: dict = {store_name: store_cls}
    exec(blocks, ns)
    return ns


def _fn_def(name: str, lines: List[str]) -> str:
    return f"def {name}() -> None:\n" + "\n".join(f"    {line}" for line in lines)


def _gen_next_lines(store_name: str, url: str, *, fixed: int | None) -> List[str]:
    """Generate compile-local-safe next_costume body (only ``<`` comparisons)."""
    lines = [f"s = {store_name}()", "if s.costume_count < 2:", "    return"]
    if fixed is not None:
        for i in range(fixed - 1):
            nxt = i + 1
            lines.append(f"if s.costume_index < {nxt}:")
            lines.append(f"    s.costume_index = {nxt}")
            lines.append(f"    s.{url} = s.{_SLOT_FIELDS[nxt]}")
            lines.append(f"    s.current_costume = s.{_NAME_FIELDS[nxt]}")
            lines.append("    return")
    else:
        for i in range(MAX_COSTUMES - 1):
            nxt = i + 1
            lines.append(f"if s.costume_index < {nxt}:")
            lines.append(f"    if s.costume_count < {nxt + 1}:")
            lines.append("        s.costume_index = 0")
            lines.append(f"        s.{url} = s.costume0")
            lines.append("        s.current_costume = s.costume_name0")
            lines.append("        return")
            lines.append(f"    s.costume_index = {nxt}")
            lines.append(f"    s.{url} = s.{_SLOT_FIELDS[nxt]}")
            lines.append(f"    s.current_costume = s.{_NAME_FIELDS[nxt]}")
            lines.append("    return")
    lines.append("s.costume_index = 0")
    lines.append(f"s.{url} = s.costume0")
    lines.append("s.current_costume = s.costume_name0")
    return lines


def _gen_save_lines(store_name: str, url: str) -> List[str]:
    lines = [f"s = {store_name}()", f"if not s.{url}:", "    return"]
    for i in range(MAX_COSTUMES):
        lines.append(f"if s.costume_count < {i + 1}:")
        lines.append(f"    s.{_SLOT_FIELDS[i]} = s.{url}")
        lines.append(f'    s.{_NAME_FIELDS[i]} = s.current_costume or "upload{i}"')
        lines.append(f"    s.costume_count = {i + 1}")
        lines.append(f"    s.costume_index = {i}")
        lines.append("    return")
    last = MAX_COSTUMES - 1
    lines.append(f"s.{_SLOT_FIELDS[last]} = s.{url}")
    lines.append(f's.{_NAME_FIELDS[last]} = s.current_costume or "upload{last}"')
    lines.append(f"s.costume_count = {MAX_COSTUMES}")
    lines.append(f"s.costume_index = {last}")
    return lines


def bind_costumes(
    store_cls: Type[Store],
    costumes: Sequence[Costume],
    *,
    url: str = "sprite_url",
) -> CostumeControls:
    """Register named costumes on Store and return compile-local handlers.

    Example (``examples/08_media``)::

        controls = bind_costumes(MediaStore, [costume("a", "a.png"), costume("b", "b.png")], url="sprite_url")
        image(controls.src(store), ...)
        button("Next", on_click=controls.next_costume)
        button("Cat", on_click=controls.switch["cat"])
    """
    _validate_field(url)
    if not costumes:
        raise ValueError("costumes must not be empty")
    if len(costumes) > MAX_COSTUMES:
        raise ValueError(f"at most {MAX_COSTUMES} costumes")

    store_name = store_cls.__name__
    names = tuple(c.name for c in costumes)

    init_lines = [f"s = {store_name}()"]
    for i, c in enumerate(costumes):
        init_lines.append(f"s.{_SLOT_FIELDS[i]} = {c.src!r}")
        init_lines.append(f"s.{_NAME_FIELDS[i]} = {c.name!r}")
    init_lines.append(f"s.costume_count = {len(costumes)}")
    init_lines.append("s.costume_index = 0")
    init_lines.append(f"s.current_costume = {costumes[0].name!r}")
    init_lines.append(f"s.{url} = {costumes[0].src!r}")
    init_src = _fn_def(f"{store_name}_init_costumes", init_lines)

    next_lines = _gen_next_lines(store_name, url, fixed=len(costumes))
    next_src = _fn_def(f"{store_name}_next_costume", next_lines)

    save_lines = _gen_save_lines(store_name, url)
    save_src = _fn_def(f"{store_name}_save_costume", save_lines)

    switch_blocks: List[str] = []
    switch_fns: Dict[str, Callable[[], None]] = {}
    for i, c in enumerate(costumes):
        safe = c.name.replace("-", "_").replace(" ", "_")
        fn_name = f"{store_name}_switch_costume_{safe}"
        block = textwrap.dedent(
            f"""
            def {fn_name}() -> None:
                s = {store_name}()
                s.costume_index = {i}
                s.{url} = s.{_SLOT_FIELDS[i]}
                s.current_costume = {c.name!r}
            """
        ).strip()
        switch_blocks.append(block)

    all_src = "\n\n".join([init_src, next_src, save_src, *switch_blocks])
    ns = _exec_handlers(store_name, store_cls, all_src)

    next_fn = _attach_source(ns[f"{store_name}_next_costume"], next_src)
    save_fn = _attach_source(ns[f"{store_name}_save_costume"], save_src)
    for i, c in enumerate(costumes):
        safe = c.name.replace("-", "_").replace(" ", "_")
        fn_name = f"{store_name}_switch_costume_{safe}"
        switch_fns[c.name] = _attach_source(ns[fn_name], switch_blocks[i])

    init_fn = _attach_source(ns[f"{store_name}_init_costumes"], init_src)
    init_fn()

    return CostumeControls(
        store_cls=store_cls,
        url_field=url,
        names=names,
        next_costume=next_fn,
        save_costume=save_fn,
        switch=switch_fns,
    )


def make_costume_handlers(
    store_cls: Type[Store],
    *,
    url: str = "sprite_url",
) -> Tuple[Callable[[], None], Callable[[], None]]:
    """Upload workflow: save current ``url`` then cycle (dynamic slots, no preset costumes)."""
    _validate_field(url)
    store_name = store_cls.__name__
    save_lines = _gen_save_lines(store_name, url)
    next_lines = _gen_next_lines(store_name, url, fixed=None)
    save_src = _fn_def(f"{store_name}_save_costume", save_lines)
    next_src = _fn_def(f"{store_name}_next_costume", next_lines)
    ns = _exec_handlers(store_name, store_cls, f"{save_src}\n\n{next_src}")
    save_fn = _attach_source(ns[f"{store_name}_save_costume"], save_src)
    next_fn = _attach_source(ns[f"{store_name}_next_costume"], next_src)
    return save_fn, next_fn
