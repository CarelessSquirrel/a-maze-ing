from file_reader import decode_cell

# takes the 2D grid of cells and draws them visually
# in the terminal using ASCII characters
# adds color to separate parts (like 42, entry & exit, path)

# V0-1
# _____________________________________

# module-level constants (or global constants)
RESET = '\033[0m'
WALL = '\033[37m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'


def paint_maze(col_idx: int, row_idx: int, entry: tuple,
               exit: tuple, path: list, is_42: bool) -> str:
    """Return the appropriate color code for a cell"""
    if (col_idx, row_idx) == entry:
        return MAGENTA
    elif (col_idx, row_idx) == exit:
        return RED
    elif path and (col_idx, row_idx) in path:
        return CYAN
    elif is_42:
        return BLUE
    return RESET


def create_grid(maze: list, width: int, height: int,
                entry: tuple, exit: tuple, path: list = None,
                wall_color: str = '') -> None:
    """Draw the grid using intersection-based approach."""
    # wc = wall_color if wall_color else WALL
    # W = f"{wc}█{RESET}"
    # W3 = f"{wc}███{RESET}"
    W = f"{wall_color}█{RESET}"
    S = " "

    # decode all cells once, save them in a 2D list
    cells = []
    for row in maze:
        cells.append([decode_cell(c) for c in row])

    def h_wall(row_idx: int, col_idx: int) -> bool:
        """Is there a horizontal wall on top of cell (col_idx, row_idx)?"""
        if row_idx >= height:
            return True  # bottom border
        if row_idx == 0:
            return True  # top border
        return cells[row_idx][col_idx]["north"]

    def v_wall(row_idx: int, col_idx: int) -> bool:
        """Is there a vertical wall on left of cell (col_idx, row_idx)?"""
        if col_idx >= width:
            return True  # right border
        if col_idx == 0:
            return True  # left border
        return cells[row_idx][col_idx]["west"]

    def corner(row_idx: int, col_idx: int) -> str:
        """Corner at intersection (col_idx, row_idx)"""
        # always draw corner on borders
        if row_idx == 0 or row_idx == height or col_idx == 0 or col_idx == width:
            return W

        
        # the east wall of the cell above-left
        top = cells[row_idx - 1][col_idx - 1]["east"] if col_idx > 0 and row_idx > 0 else False
        # the east wall of the cell below-left
        bottom = cells[row_idx][col_idx - 1]["east"] if col_idx > 0 and row_idx < height else False
        # the south wall of the cell above-left
        left = cells[row_idx - 1][col_idx - 1]["south"] if col_idx > 0 and row_idx > 0 else False
        # the south wall of the cell above-right
        right = cells[row_idx - 1][col_idx]["south"] if col_idx < width and row_idx > 0 else False

        if any([top, bottom, left, right]):
            return W
        return S

    for row_idx in range(height):
        # top line for this row
        top_line = ""
        for col_idx in range(width):
            top_line += corner(row_idx, col_idx)
            if h_wall(row_idx, col_idx):
                # top_line += W3
                top_line += f"{wall_color}███{RESET}"
            else:
                top_line += S + S + S
        top_line += corner(row_idx, width)
        print(top_line)

        # middle line for this row
        mid_line = ""
        for col_idx in range(width):
            left = W if v_wall(row_idx, col_idx) else S
            cell = cells[row_idx][col_idx]
            is_42 = all(cell[w] for w in ["north", "east", "south", "west"])
            color = paint_maze(col_idx, row_idx, entry, exit, path, is_42)
            if (col_idx, row_idx) == entry:
                mid_line += f"{left}{color} E {RESET}"
            elif (col_idx, row_idx) == exit:
                mid_line += f"{left}{color} X {RESET}"
            elif path and (col_idx, row_idx) in path:
                mid_line += f"{left}{color} ● {RESET}"
            elif is_42:
                mid_line += f"{left}{color}███{RESET}"
            else:
                mid_line += f"{left}   "
        mid_line += W
        print(mid_line)

    # final bottom line
    bottom = ""
    for col_idx in range(width):
        bottom += corner(height, col_idx)
        # bottom += W3
        bottom += f"{wall_color}███{RESET}"
    bottom += corner(height, width)
    print(bottom)
