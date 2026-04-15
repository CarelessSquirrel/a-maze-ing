from __future__ import annotations

import sys
from typing import Any, Dict

from config_parser import parse_config
from file_reader import process_directions
from mazegen import encode_maze, generate_maze, solve_maze, write_maze_file
from jacobs_menu import run_menu


def main() -> None:
    # Accept an optional path to the config file as a CLI argument
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'config.txt'

    try:
        config: Dict[str, Any] = parse_config(config_file)
    except FileNotFoundError:
        print(f"Error: config file '{config_file}' not found.")
        sys.exit(1)
    except ValueError as exc:
        print(f"Configuration error: {exc}")
        sys.exit(1)

    # Generate the first maze and write it to the output file
    cells, has_42 = _new_maze(config)

    run_menu(cells, config)


def _new_maze(config: Dict[str, Any]):  # type: ignore[return]
    """Generate a fresh maze, solve it, persist it, and return (cells, has_42)."""
    cells, has_42 = generate_maze(
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

    if path is None:
        # Should never happen with a valid perfect maze, but be safe
        print("Warning: no solution found for this maze.")
        path = []

    write_maze_file(
        config['OUTPUT_FILE'],
        cells,
        config['ENTRY'],
        config['EXIT'],
        path,
    )

    return cells, has_42


if __name__ == '__main__':
    main()
