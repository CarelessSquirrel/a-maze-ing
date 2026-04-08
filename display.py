# takes the 2D grid of cells and draws them visually
# in the terminal using ASCII characters

def create_grid(maze: list, width: int, height: int) -> None:
    """
    Draw the grid with our given maze data using block symbol
    """
    # we are skipping bottom line as that is the following rows top line
    # for each row in maze
        # draw the top line 
            # for each cell in a row:
                # check if north wall exists & draw █████ or spaces if no wall
        # draw the midle line:
            # for each cell in row:
                # check if wall exists & draw █
                # draw 3 spcaes (the middle bit)
                # check if east wall exists & draw █
    # after all the ows:
        # draw the final bottom line for the last row
    pass
