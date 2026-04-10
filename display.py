from file_reader import decode_cell

# takes the 2D grid of cells and draws them visually
# in the terminal using ASCII characters

RESET = '\033[0m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RED = '\033[91m'
YELLOW = '\033[93m'


def create_grid(maze: list,
                width: int,
                height: int,
                entry: tuple,
                exit: tuple,
                path: list) -> None:

    """
    Draw the grid with our given maze data using block symbol
    """
    # Structure
    # _____________________________________
    # we are skipping bottom line as that is the following rows top line
    # for each row in maze
        # draw the top line 
            # for each cell in a row:
                # check if north wall exists & draw cell or spaces if no wall
        # draw the midle line:
            # for each cell in row:
                # check if wall exists & draw █
                # draw 3 spcaes (the middle bit)
                # check if east wall exists & draw █
    # after all the ows:
        # draw the final bottom line for the last row

    #V1
    # _____________________________________
    # for row in maze:
    #     for cell in row:
    #         current_cell = decode_cell(cell)
    #         if current_cell["north"] is True:
    #             print("████", end='')
    #         else:
    #             corner_left = "█" if current_cell["west"] else " "
    #             print(f"{corner_left}   ", end='')
    #     print("█")
    #     for cell in row:
    #         current_cell = decode_cell(cell)
    #         # left = "█" if current_cell["west"] else " "
    #         # right = "█" if current_cell["east"] else " "
    #         # print(f"{left}  {right}", end='')
    #         left = "█" if current_cell["west"] else " "
    #         print(f"{left}   ", end='')
    #     print("█")
    # # print bottom border
    # print("█" * (width * 4 + 1))

    # V2
    # _____________________________________
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            current_cell = decode_cell(cell)
            left = "█" if current_cell["west"] else " "
            is_42 = all(current_cell[w] for w in ["north", "east", "south", "west"])
            if (col_idx, row_idx) == entry:
                print(f"{MAGENTA}{left} E {RESET}", end='')
            elif (col_idx, row_idx) == exit:
                print(f"{RED}{left} X {RESET}", end='')
            elif path and (col_idx, row_idx) in path:
                print(f"{CYAN}{left} * {RESET}", end='')
            elif is_42:
                print(f"{YELLOW}{left}███{RESET}", end='')
            else:
                print(f"{left}   ", end='')
        print("█")
    print("█" * (width * 4 + 1))

    # V3
    # _____________________________________
    # for row in maze:
    #     for cell in row:
    #         current_cell = decode_cell(cell)
    #         if current_cell["north"] is True:
    #             print("████", end='')
    #         else:
    #             print("    ", end='')
    #         if current_cell["west"] is True or current_cell["east"] is True:
    #             if current_cell["west"] is True:
    #                 left = "█"
    #             else:
    #                 left = " "
    #             if current_cell["east"] is True:
    #                 right = "█"
    #             else:
    #                 right = " "
    #             print(f"{left}  {right}", end='')
    #     print()

    def mark_entry_and_exit(maze: list, entry, ext) -> None:
        pass
