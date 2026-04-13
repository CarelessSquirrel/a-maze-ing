from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Tuple

from display import create_grid
from file_reader import process_directions
from mazegen import encode_maze, generate_maze, solve_maze, write_maze_file

# Named wall-colour options shown in the colour picker submenu
_WALL_COLORS: List[Tuple[str, str]] = [
    ('Default (white)', ''),
    ('Blue',            '\033[34m'),
    ('Green',           '\033[32m'),
    ('Red',             '\033[91m'),
    ('Cyan',            '\033[96m'),
    ('Magenta',         '\033[95m'),
]


def run_menu(
    initial_cells: List[List[int]],
    config: Dict[str, Any],
) -> None:
    """
    Main interactive loop.

    Displays the maze and a menu, then reacts to user input until the user
    chooses to quit.  Mandatory interactions (per evaluation sheet):
      1. Re-generate a new maze
      2. Toggle the solution path on / off
      3. Change the colour of the walls
    """
    cells = initial_cells
    show_path: bool = False
    wall_color: str = ''   # empty string = default terminal colour

    while True:
        _clear()
        _render(cells, config, show_path, wall_color)
        _print_menu(show_path, wall_color)

        choice = input('> ').strip()

        if choice == '1':
            cells = _regenerate(config)
        elif choice == '2':
            show_path = not show_path
        elif choice == '3':
            wall_color = _pick_color()
        elif choice == '4':
            print('Goodbye!')
            break
        else:
            pass


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _regenerate(config: Dict[str, Any]) -> List[List[int]]:
    """Generate a new maze, persist it, and return the new cells grid."""
    cells, _ = generate_maze(
        config['WIDTH'],
        config['HEIGHT'],
        config['ENTRY'],
        config['EXIT'],
        perfect=config['PERFECT'],
    )
    path = solve_maze(
        cells,
        config['ENTRY'],
        config['EXIT'],
        config['WIDTH'],
        config['HEIGHT'],
    )
    write_maze_file(
        config['OUTPUT_FILE'],
        cells,
        config['ENTRY'],
        config['EXIT'],
        path if path is not None else [],
    )
    return cells


def _render(
    cells: List[List[int]],
    config: Dict[str, Any],
    show_path: bool,
    wall_color: str,
) -> None:
    """Convert cells to the hex-string grid Agnes's display expects, then draw."""
    hex_grid = encode_maze(cells)

    coord_path: List[Tuple[int, int]] = []
    if show_path:
        path_dirs: Optional[List[str]] = solve_maze(
            cells,
            config['ENTRY'],
            config['EXIT'],
            config['WIDTH'],
            config['HEIGHT'],
        )
        if path_dirs:
            coord_path = process_directions(path_dirs, config['ENTRY'])

    create_grid(
        hex_grid,
        config['WIDTH'],
        config['HEIGHT'],
        config['ENTRY'],
        config['EXIT'],
        coord_path,
        wall_color,
    )


def _print_menu(show_path: bool, wall_color: str) -> None:
    path_state = 'ON' if show_path else 'OFF'
    color_name = next(
        (name for name, code in _WALL_COLORS if code == wall_color),
        'Custom',
    )
    print()
    print('┌─ A-Maze-ing ──────────────────────┐')
    print('│  1. Re-generate maze              │')
    print(f'│  2. Toggle solution path  [{path_state:>3}]   │')
    print(f'│  3. Change wall colour  [{color_name:<9}]│')
    print('│  4. Quit                          │')
    print('└───────────────────────────────────┘')


def _pick_color() -> str:
    """Show a colour submenu and return the chosen ANSI escape code."""
    _clear()
    print('Choose a wall colour:\n')
    for idx, (name, _) in enumerate(_WALL_COLORS, start=1):
        print(f'  {idx}. {name}')
    raw = input('\n> ').strip()
    try:
        chosen = int(raw) - 1
        if 0 <= chosen < len(_WALL_COLORS):
            return _WALL_COLORS[chosen][1]
    except ValueError:
        pass
    return ''   # fall back to default on bad input


def _clear() -> None:
    os.system('clear' if os.name == 'posix' else 'cls')
