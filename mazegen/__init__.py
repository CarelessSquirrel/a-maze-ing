"""
mazegen — reusable maze-generation package for the a-maze-ing project.

Public API
----------
generate_maze(width, height, entry, exit_, perfect, seed)
    Generate a maze and return (cells, has_42).

solve_maze(cells, entry, exit_, width, height)
    BFS shortest-path solver.  Returns a list of direction chars or None.

encode_maze(cells)
    Convert the int grid to a list of hex strings for display / file output.

write_maze_file(filename, cells, entry, exit_, path)
    Persist the maze + metadata to disk in the standard project format.
"""

from mazegen.generator import generate_maze, has_open_zone
from mazegen.solver import solve_maze
from mazegen.writer import encode_maze, write_maze_file

__all__ = [
    'generate_maze',
    'has_open_zone',
    'solve_maze',
    'encode_maze',
    'write_maze_file',
]
