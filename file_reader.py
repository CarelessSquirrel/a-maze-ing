# Functions for reading and processing the maze output file


def read_maze_file(filename: str) -> tuple:
    """
    Reads the maze output file and returns the maze grid
    as a 2D list of hex characters + the entry + exit +
    solution path.
    """
    pass


def decode_cell(hex_char: str) -> dict:
    """
    Take the 2D grid created in read_maze_file() and turn 
    the hex charcters into walls
    """
    pass


def process_directions(path: str) -> list:
    """
    take the direction string and put coordinates from it
    into a list, they will represent the solution path
    """
    pass
