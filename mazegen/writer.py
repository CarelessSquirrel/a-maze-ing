from __future__ import annotations

from typing import List, Tuple


def encode_maze(cells: List[List[int]]) -> List[str]:
    """
    Convert the 2-D int grid produced by the generator into a list of
    hex-encoded strings (one string per row, one uppercase hex character
    per cell).  This is the format Agnes's file_reader expects.
    """
    return [''.join(format(cell, 'X') for cell in row) for row in cells]


def write_maze_file(
    filename: str,
    cells: List[List[int]],
    entry: Tuple[int, int],
    exit_: Tuple[int, int],
    path: List[str],
) -> None:
    """
    Write the maze to *filename* in the standard project format:

        <HEIGHT rows of WIDTH hex chars>
        <empty line>
        x,y          <- entry
        x,y          <- exit
        NSEWNSEW...  <- shortest-path direction string
    """
    rows = encode_maze(cells)
    with open(filename, 'w') as fh:
        for row in rows:
            fh.write(row + '\n')
        fh.write('\n')
        fh.write(f'{entry[0]},{entry[1]}\n')
        fh.write(f'{exit_[0]},{exit_[1]}\n')
        fh.write(''.join(path) + '\n')
