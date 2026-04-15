"""Read and process maze.txt file and convert it to display"""


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


# A cell is one "pixel" of the maze that represents where a wall will be
def decode_cell(cell: str) -> dict:
    """
    Take the 2D grid created in read_maze_file() and turn
    the hex charcters into walls
    """
    # take the first character from the first maze line
    # convert it from a hex to a regular int
    value = int(cell, 16)
    # check each of the 4 bits of this int with a mask:
    # LSB - least significant bit
        # bit 0 (LSB)= north wall
        # bit 1 = east wall
        # bit 2 = south wall
        # bit 3 = west wall
    north = bool(value & 1)   # checks bit 0
    east = bool(value & 2)    # checks bit 1
    south = bool(value & 4)   # checks bit 2
    west = bool(value & 8)    # checks bit 3
    # return a dict something like:
    # {"north": True, "east": False, "south": True, "west": False}
    cell_walls = {
        "north": north,
        "east": east,
        "south": south,
        "west": west
        }
    return (cell_walls)


def process_directions(path: list, entry: tuple) -> list:
    """
    take the direction string and put coordinates from it
    into a list, they will represent the solution path
    """
    current_pos = entry
    coordinates = []
    for direction in path:
        x, y = current_pos
        if direction == 'S':
            current_pos = (x, y + 1)
        if direction == 'N':
            current_pos = (x, y - 1)
        if direction == 'E':
            current_pos = (x + 1, y)
        if direction == 'W':
            current_pos = (x - 1, y)
        coordinates.append(current_pos)
    return (coordinates)
