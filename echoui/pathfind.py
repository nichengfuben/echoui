"""Grid pathfinding."""

from __future__ import annotations

import heapq
from typing import Callable, List, Optional, Tuple


def astar(
    start: Tuple[int, int],
    goal: Tuple[int, int],
    *,
    passable: Callable[[int, int], bool],
    heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float] | None = None,
) -> Optional[List[Tuple[int, int]]]:
    h = heuristic or (lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1]))
    open_set: list[tuple[float, Tuple[int, int]]] = [(h(start, goal), start)]
    came_from: dict[Tuple[int, int], Tuple[int, int]] = {}
    g_score: dict[Tuple[int, int], float] = {start: 0}
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return _reconstruct(came_from, current)
        for nb in _neighbors(current):
            if not passable(*nb):
                continue
            tentative = g_score[current] + 1
            if tentative < g_score.get(nb, float("inf")):
                came_from[nb] = current
                g_score[nb] = tentative
                f = tentative + h(nb, goal)
                heapq.heappush(open_set, (f, nb))
    return None


def _neighbors(pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = pos
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def _reconstruct(came_from: dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
