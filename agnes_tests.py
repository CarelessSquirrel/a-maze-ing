from file_reader import read_maze_file
from file_reader import decode_cell
from file_reader import process_directions
from display import create_grid

# a place to test my functions

# test file_reader

# directions = ['S', 'W', 'S', 'E', 'S', 'W', 'S', 'E', 'S', 'W', 'S', 'S', 'S', 'E', 'E', 'S', 'E', 'E', 'E', 'E', 'N', 'E', 'E', 'S', 'E', 'S', 'E', 'E', 'S', 'S', 'S', 'E', 'E', 'E', 'S', 'S', 'S', 'E', 'E', 'E', 'N', 'N', 'E', 'N', 'E', 'E']

# print(read_maze_file("temp_mock_maze.txt"))
# print(decode_cell('A'))
# print(process_directions(directions, (1, 1)))

# test display

result = read_maze_file("temp_mock_maze.txt")
maze = result[0]
create_grid(maze, 25, 20)
