"""Data display — virtual lists and tables."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Generic, List, Optional, TypeVar

T = TypeVar("T")


@dataclass
class VirtualList(Generic[T]):
    """Windowed list with O(1) scroll offset math."""

    items: List[T] = field(default_factory=list)
    item_height: int = 40
    viewport_height: int = 400
    scroll_top: float = 0
    render_item: Optional[Callable[[T, int], Any]] = None

    @property
    def total_height(self) -> int:
        return len(self.items) * self.item_height

    @property
    def visible_count(self) -> int:
        return max(1, int(self.viewport_height / self.item_height) + 2)

    @property
    def start_index(self) -> int:
        return max(0, int(self.scroll_top // self.item_height))

    @property
    def end_index(self) -> int:
        return min(len(self.items), self.start_index + self.visible_count)

    def visible_items(self) -> List[tuple[int, T]]:
        return [(i, self.items[i]) for i in range(self.start_index, self.end_index)]

    def scroll_to(self, index: int) -> None:
        self.scroll_top = max(0, min(index * self.item_height, self.total_height - self.viewport_height))

    def scroll_by(self, delta: float) -> None:
        self.scroll_to(int((self.scroll_top + delta) // self.item_height))


@dataclass
class DataTable:
    columns: List[dict[str, Any]] = field(default_factory=list)
    rows: List[dict[str, Any]] = field(default_factory=list)
    sort_key: Optional[str] = None
    sort_asc: bool = True

    def sort_by(self, key: str) -> None:
        if self.sort_key == key:
            self.sort_asc = not self.sort_asc
        else:
            self.sort_key = key
            self.sort_asc = True
        self.rows.sort(key=lambda r: r.get(key, ""), reverse=not self.sort_asc)
