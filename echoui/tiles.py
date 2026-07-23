"""Tile map utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class TileMap:
    cols: int
    rows: int
    tile_size: int
    data: List[int]

    def get(self, col: int, row: int) -> int:
        if col < 0 or row < 0 or col >= self.cols or row >= self.rows:
            return -1
        return self.data[row * self.cols + col]

    def set(self, col: int, row: int, value: int) -> None:
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.data[row * self.cols + col] = value

    def world_to_tile(self, x: float, y: float) -> tuple[int, int]:
        return int(x // self.tile_size), int(y // self.tile_size)

    def tile_to_world(self, col: int, row: int) -> tuple[float, float]:
        return col * self.tile_size, row * self.tile_size


def tilemap(cols: int, rows: int, tile_size: int = 32, fill: int = 0) -> TileMap:
    return TileMap(cols=cols, rows=rows, tile_size=tile_size, data=[fill] * (cols * rows))
