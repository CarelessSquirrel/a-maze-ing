from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional, Tuple

# Mirror the same bit masks used by generator.py
NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8

# direction name -> (dx, dy, wall bit that blocks movement in that direction)
_MOVES: Dict[str, Tuple[int, int, int]] = {
    'N': (0,  -1, NORTH),
    'E': (1,   0, EAST),
    'S': (0,   1, SOUTH),
    'W': (-1,  0, WEST),
}


def solve_maze(
    cells: List[List[int]],
    entry: Tuple[int, int],
    exit_: Tuple[int, int],
    width: int,
    height: int,
) -> Optional[List[str]]:
    """
    BFS shortest-path search from *entry* to *exit_*.

    Returns a list of direction characters ['N','E','S','W', ...] representing
    the shortest path, or None if no path exists (e.g. isolated exit cell).

    BFS guarantees the shortest path in an unweighted graph.
    """
    queue: deque[Tuple[Tuple[int, int], List[str]]] = deque([(entry, [])])
    visited: set[Tuple[int, int]] = {entry}

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == exit_:
            return path

        for dir_name, (dx, dy, wall_bit) in _MOVES.items():
            if cells[y][x] & wall_bit:
                # wall is present — cannot move in this direction
                continue
            nx, ny = x + dx, y + dy
            if (0 <= nx < width and 0 <= ny < height and (nx, ny)
                    not in visited):
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [dir_name]))

    return None   # maze has no solution (should not happen for a valid maze)
