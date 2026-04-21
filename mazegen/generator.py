from __future__ import annotations

import random
from typing import List, Optional, Set, Tuple

# Wall bit masks — each cell is a 4-bit integer stored in a 2D grid.
# A set bit means the wall EXISTS (is closed).  Clearing a bit carves a passage
NORTH: int = 1   # bit 0
EAST: int = 2   # bit 1
SOUTH: int = 4   # bit 2
WEST: int = 8   # bit 3

# (dx, dy, wall on current cell, opposite wall on neighbour)
_MOVES: List[Tuple[int, int, int, int]] = [
    (0, -1, NORTH, SOUTH),
    (1,  0, EAST,  WEST),
    (0,  1, SOUTH, NORTH),
    (-1, 0, WEST,  EAST),
]

# --- "42" pixel-art pattern (1 = fully-walled cell, 0 = normal cell) ---
# Layout: "4" (3 wide) + gap (1 wide) + "2" (3 wide) = 7 columns, 5 rows
_PATTERN_42: List[List[int]] = [
    [1, 0, 1,  0,  1, 1, 1],
    [1, 1, 1,  0,  0, 0, 1],
    [0, 0, 1,  0,  1, 1, 1],
    [0, 0, 1,  0,  1, 0, 0],
    [0, 0, 1,  0,  1, 1, 1],
]
_PAT_W: int = 7
_PAT_H: int = 5
# Min maze dim required to embed the pattern with 2-cell padding on each side
_MIN_W: int = _PAT_W + 4
_MIN_H: int = _PAT_H + 4


def generate_maze(
    width: int,
    height: int,
    entry: Tuple[int, int],
    exit_: Tuple[int, int],
    perfect: bool = True,
    seed: Optional[int] = None,
) -> Tuple[List[List[int]], bool]:
    """
    Generate a maze using iterative depth-first search (randomised DFS).

    Returns (cells, has_42) where:
      - cells  : 2-D list of ints (height rows x width cols).  Each int is a
                 4-bit wall mask (NORTH/EAST/SOUTH/WEST).
      - has_42 : True when the '42' pattern was successfully embedded.

    A perfect maze (spanning tree, no loops) is produced when perfect=True.
    When perfect=False a small number of extra passages are carved after the
    spanning tree is built, subject to the no-3x3-open-zone constraint.
    """
    if seed is not None:
        random.seed(seed)

    # Start with every wall closed (0xF = all four walls present)
    cells: List[List[int]] = [[0xF] * width for _ in range(height)]

    # ------------------------------------------------------------------
    # Embed the '42' pattern before generation so DFS never enters those
    # cells.  Pattern cells are pre-marked visited.
    # ------------------------------------------------------------------
    pattern_cells: Set[Tuple[int, int]] = set()
    has_42 = _place_42(cells, width, height, pattern_cells)
    if not has_42:
        print("Maze is too small to display the '42' pattern.")

    # ------------------------------------------------------------------
    # Iterative DFS (randomised Recursive Backtracker)
    # All reachable cells will be visited; pattern cells are skipped.
    # Because this builds a spanning tree, a 3x3 open zone is impossible
    # by construction (it would require 4 extra edges / cycles).
    # ------------------------------------------------------------------
    visited: List[List[bool]] = [[False] * width for _ in range(height)]
    for px, py in pattern_cells:
        visited[py][px] = True

    sx, sy = entry
    visited[sy][sx] = True
    stack: List[Tuple[int, int]] = [(sx, sy)]

    while stack:
        x, y = stack[-1]
        neighbours = [
            (x + dx, y + dy, wall, opp)
            for dx, dy, wall, opp in _MOVES
            if 0 <= x + dx < width
            and 0 <= y + dy < height
            and not visited[y + dy][x + dx]
        ]
        if neighbours:
            nx, ny, wall, opp = random.choice(neighbours)
            cells[y][x] &= ~wall          # remove wall on current cell
            cells[ny][nx] &= ~opp         # remove opposite wall on neighbour
            visited[ny][nx] = True
            stack.append((nx, ny))
        else:
            stack.pop()

    # ------------------------------------------------------------------
    # Imperfect maze: add a handful of extra passages (loops).
    # Each candidate wall is only removed if it does NOT create a 3x3
    # open zone anywhere in the maze.
    # ------------------------------------------------------------------
    if not perfect:
        _add_loops(cells, width, height, pattern_cells)

    return cells, has_42


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _place_42(
    cells: List[List[int]],
    width: int,
    height: int,
    pattern_cells: Set[Tuple[int, int]],
) -> bool:
    """
    Stamp the '42' pixel pattern into *cells*, centred in the maze.
    Populates *pattern_cells* with the (x, y) positions of stamped cells.
    Returns False (and leaves the maze untouched) if the maze is too small.
    """
    if width < _MIN_W or height < _MIN_H:
        return False

    ox: int = (width - _PAT_W) // 2
    oy: int = (height - _PAT_H) // 2

    for ry in range(_PAT_H):
        for rx in range(_PAT_W):
            if _PATTERN_42[ry][rx]:
                cx, cy = ox + rx, oy + ry
                cells[cy][cx] = 0xF           # all walls closed
                pattern_cells.add((cx, cy))

    return True


def _is_open_zone(cells: List[List[int]], gx: int, gy: int) -> bool:
    """
    Return True if the 3x3 sub-grid whose top-left corner is (gx, gy)
    contains no interior walls (every adjacent pair of cells is connected).
    """
    for y in range(gy, gy + 3):
        for x in range(gx, gx + 3):
            if x < gx + 2 and cells[y][x] & EAST:
                return False
            if y < gy + 2 and cells[y][x] & SOUTH:
                return False
    return True


def has_open_zone(cells: List[List[int]], width: int, height: int) -> bool:
    """
    Scan the whole maze for 3x3 open zones.
    Returns True if at least one exists (should never happen in a perfect maze)
    Public so a_maze_ing.py can use it for a debug assertion if needed.
    """
    for gy in range(height - 2):
        for gx in range(width - 2):
            if _is_open_zone(cells, gx, gy):
                return True
    return False


def _add_loops(
    cells: List[List[int]],
    width: int,
    height: int,
    pattern_cells: Set[Tuple[int, int]],
    loop_factor: float = 0.05,
) -> None:
    """
    Remove a fraction of remaining interior walls to introduce cycles.
    Only removes a wall if doing so does NOT create a 3x3 open zone.
    """
    # Build a list of all interior walls that still exist
    candidates: List[Tuple[int, int, int, int, int, int]] = []
    for y in range(height):
        for x in range(width):
            if (x, y) in pattern_cells:
                continue
            if (x + 1 < width and (x + 1, y) not in pattern_cells
                    and cells[y][x] & EAST):
                candidates.append((x, y, x + 1, y, EAST, WEST))
            if (y + 1 < height and (x, y + 1) not in pattern_cells
                    and cells[y][x] & SOUTH):
                candidates.append((x, y, x, y + 1, SOUTH, NORTH))

    random.shuffle(candidates)
    target = max(1, int(len(candidates) * loop_factor))
    added = 0

    for x, y, nx, ny, wall, opp in candidates:
        if added >= target:
            break
        # Tentatively remove the wall
        cells[y][x] &= ~wall
        cells[ny][nx] &= ~opp
        # Check every 3x3 grid that overlaps both cells
        violation = False
        for gy in range(max(0, min(y, ny) - 2), min(height - 2,
                                                    max(y, ny) + 1)):
            for gx in range(max(0, min(x, nx) - 2), min(width - 2,
                                                        max(x, nx) + 1)):
                if _is_open_zone(cells, gx, gy):
                    violation = True
                    break
            if violation:
                break
        if violation:
            # Revert
            cells[y][x] |= wall
            cells[ny][nx] |= opp
        else:
            added += 1
