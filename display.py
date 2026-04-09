from file_reader import decode_cell

# takes the 2D grid of cells and draws them visually
# in the terminal using ASCII characters

def create_grid(maze: list, width: int, height: int) -> None:
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
    prev_row = None
    for row in maze:
        for i, cell in enumerate(row):
            current_cell = decode_cell(cell)
            if current_cell["north"] is True:
                print("████", end='')
            else:
                if prev_row is not None:
                    above_cell = decode_cell(prev_row[i])
                    corner = "█" if above_cell["south"] or current_cell["west"] else " "
                else:
                    corner = " "
                print(f"{corner}   ", end='')
        print("█")
        for cell in row:
            current_cell = decode_cell(cell)
            left = "█" if current_cell["west"] else " "
            print(f"{left}   ", end='')
        print("█")
        prev_row = row
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
