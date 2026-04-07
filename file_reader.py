# Functions for reading and processing the maze output file
# First two lines:
# 9515391539551795151151153
# EBABAE812853C1412BA812812


def read_maze_file(filename: str) -> tuple:
    """
    Reads the maze output file and returns the maze grid
    as a 2D list of hex characters + the entry + exit +
    solution path.
    """

    with open(filename, 'r') as file:
        lines = file.readlines()
    # now we have a list called lines that contains everything:
    # maze in hex chars, entry, exit, path
    # defining a 2D list of lists to save as maze
    maze = []
    entry = []
    exit = []
    path = []
    empty_line_index = lines.index('\n')
    for line in lines:
        if line != '\n':
            maze.append(list(line.strip()))
        if line == '\n':
            break

    # save the first line after empty line as tuple coordinates for entry
    coordinates_entry = lines[empty_line_index + 1].split(",")
    entry = tuple(int(x) for x in coordinates_entry)
    # save the following line as coordinates for exit
    coordinates_exit = lines[empty_line_index + 2].split(",")
    exit = tuple(int(x) for x in coordinates_exit)
    # save the following line as a list of the path
    path = list(lines[empty_line_index + 3].strip())

    return (maze, entry, exit, path)


def decode_cell(maze: str) -> dict:
    """
    Take the 2D grid created in read_maze_file() and turn 
    the hex charcters into walls
    """
    # take the first character from the first maze line
    # convert it from a hex to a regular int
    # check each of the 4 bits of this int:
    # LSB - least significant bit
        # bit 0 (LSB)= north wall
        # bit 1 = east wall
        # bit 2 = south wall
        # bit 3 = west wall
    # return a dict something like:
    # {"north": True, "east": False, "south": True, "west": False}
    pass


def process_directions(path: str) -> list:
    """
    take the direction string and put coordinates from it
    into a list, they will represent the solution path
    """
    pass

