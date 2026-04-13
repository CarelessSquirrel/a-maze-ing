from file_reader import decode_cell

# takes the 2D grid of cells and draws them visually
# in the terminal using ASCII characters
# adds color to separate parts (like 42, entry & exit, path)

# V0-1
# _____________________________________

RESET = '\033[0m'
WALL = '\033[37m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RED = '\033[91m'
YELLOW = '\033[93m'


def paint_maze(col_idx: int, row_idx: int, entry: tuple,
               exit: tuple, path: list, is_42: bool) -> str:
    """Return the appropriate color code for a cell."""
    if (col_idx, row_idx) == entry:
        return MAGENTA
    elif (col_idx, row_idx) == exit:
        return RED
    elif path and (col_idx, row_idx) in path:
        return CYAN
    elif is_42:
        return YELLOW
    return RESET


def create_grid(maze: list, width: int, height: int,
                entry: tuple, exit: tuple, path: list = None) -> None:
    """Draw the grid using intersection-based approach."""
    W = f"{WALL}█{RESET}"
    S = " "

    # decode all cells once
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
        
        top = cells[row_idx - 1][col_idx - 1]["east"] if col_idx > 0 and row_idx > 0 else False
        bottom = cells[row_idx][col_idx - 1]["east"] if col_idx > 0 and row_idx < height else False
        left = cells[row_idx - 1][col_idx - 1]["south"] if col_idx > 0 and row_idx > 0 else False
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
                top_line += f"{WALL}███{RESET}"
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
                mid_line += f"{left}{color} * {RESET}"
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
        bottom += f"{WALL}███{RESET}"
    bottom += corner(height, width)
    print(bottom)

# V0
# _____________________________________


# def paint_maze(col_idx: int, row_idx: int, entry: tuple,
#                exit: tuple, path: list, is_42: bool) -> str:
#     """Return the appropriate color code for a cell."""
#     if (col_idx, row_idx) == entry:
#         return MAGENTA
#     elif (col_idx, row_idx) == exit:
#         return RED
#     elif path and (col_idx, row_idx) in path:
#         return CYAN
#     elif is_42:
#         return YELLOW
#     return RESET


# def create_grid(maze: list, width: int, height: int,
#                 entry: tuple, exit: tuple, path: list = None) -> None:
#     """Draw the grid with maze data using block symbols."""
#     W = f"{WALL}█{RESET}"
#     S = " "

#     def get_corner(row_idx: int, col_idx: int) -> str:
#         """Return corner character based on surrounding walls."""
#           pass

#     for row_idx, row in enumerate(maze):
#         top_line = ""
#         mid_line = ""

#         for col_idx, cell in enumerate(row):
#             current_cell = decode_cell(cell)
#             is_42 = all(current_cell[w] for w in
#                         ["north", "east", "south", "west"])
#             color = paint_maze(col_idx, row_idx, entry, exit, path, is_42)

#             # build top line
#             corner = get_corner(row_idx, col_idx)
#             if current_cell["north"]:
#                 top_line += corner + f"{WALL}███{RESET}"
#             else:
#                 top_line += corner + S + S + S

#             # build mid line
#

#         # final right wall
#         last_cell = decode_cell(row[-1])
#         corner_end = W if any([
#             last_cell["north"],
#             last_cell["east"],
#             row_idx > 0 and decode_cell(maze[row_idx - 1][-1])["south"]
#         ]) else S
#         top_line += corner_end
#         mid_line += W
#         print(top_line)
#         print(mid_line)

#     # bottom line
#     bottom = ""
#     for col_idx, cell in enumerate(maze[-1]):
#         current_cell = decode_cell(cell)
#         corner = W if (current_cell["south"] or current_cell["west"]) else S
#         bottom += corner + (f"{WALL}███{RESET}" if current_cell["south"] else S + S + S)
#     bottom += W
#     print(bottom)

# V1
# _____________________________________


# def paint_maze(col_idx: int, row_idx: int, entry: tuple,
#                exit: tuple, path: list, is_42: bool) -> str:
#     """Return the appropriate color code for a cell."""
#     if (col_idx, row_idx) == entry:
#         return MAGENTA
#     elif (col_idx, row_idx) == exit:
#         return RED
#     elif path and (col_idx, row_idx) in path:
#         return CYAN
#     elif is_42:
#         return YELLOW
#     return RESET


# def create_grid(maze: list, width: int, height: int,
#                 entry: tuple, exit: tuple, path: list = None) -> None:
#     """Draw the grid with maze data using block symbols."""
#     WALL_CHAR = f"{WALL}█{RESET}"
#     SPACE = " "

#     for row_idx, row in enumerate(maze):
#         for cell in row:
#             current_cell = decode_cell(cell)
#             if current_cell["north"]:
#                 print(f"{WALL}████{RESET}", end='')
#             else:
#                 print(f"{WALL}█{RESET}   ", end='')
#         print(f"{WALL}█{RESET}")
#         for col_idx, cell in enumerate(row):
#             current_cell = decode_cell(cell)
#             left = f"{WALL}█{RESET}" if current_cell["west"] else SPACE
#             is_42 = all(current_cell[w] for w in ["north", "east", "south", "west"])
#             color = paint_maze(col_idx, row_idx, entry, exit, path, is_42)
#             if (col_idx, row_idx) == entry:
#                 print(f"{left}{color} E {RESET}", end='')
#             elif (col_idx, row_idx) == exit:
#                 print(f"{left}{color} X {RESET}", end='')
#             elif path and (col_idx, row_idx) in path:
#                 print(f"{left}{color} * {RESET}", end='')
#             elif is_42:
#                 print(f"{left}{color}███{RESET}", end='')
#             else:
#                 print(f"{left}   ", end='')
#         print(f"{WALL}█{RESET}")
#     print(f"{WALL}" + "█" * (width * 4 + 1) + f"{RESET}")

# ________________________________________

# RESET = '\033[0m'
# CYAN = '\033[96m'
# MAGENTA = '\033[95m'
# RED = '\033[91m'
# YELLOW = '\033[93m'


# def paint_maze(col_idx: int, row_idx: int, entry: tuple, exit: tuple, path: list, is_42: bool) -> str:
#     """Return the matching color code for a cell."""
#     if (col_idx, row_idx) == entry:
#         return MAGENTA
#     elif (col_idx, row_idx) == exit:
#         return RED
#     elif path and (col_idx, row_idx) in path:
#         return CYAN
#     elif is_42:
#         return YELLOW
#     return RESET

    # V2
    # _____________________________________
    # for row_idx, row in enumerate(maze):
    #     for cell in row:
    #         current_cell = decode_cell(cell)
    #         if current_cell["north"]:
    #             print("████", end='')
    #         else:
    #             print("█   ", end='')
    #     print("█")
    #     for col_idx, cell in enumerate(row):
    #         current_cell = decode_cell(cell)
    #         left = "█" if current_cell["west"] else " "
    #         is_42 = all(current_cell[w] for w in ["north", "east", "south", "west"])
    #         color = paint_maze(col_idx, row_idx, entry, exit, path, is_42)
    #         if (col_idx, row_idx) == entry:
    #             print(f"{color}{left} E {RESET}", end='')
    #         elif (col_idx, row_idx) == exit:
    #             print(f"{color}{left} X {RESET}", end='')
    #         elif path and (col_idx, row_idx) in path:
    #             print(f"{color}{left} * {RESET}", end='')
    #         elif is_42:
    #             print(f"{color}{left}███{RESET}", end='')
    #         else:
    #             print(f"{left}   ", end='')
    #     print("█")
    # print("█" * (width * 4 + 1))

